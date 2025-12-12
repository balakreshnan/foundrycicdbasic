import asyncio
import os
from random import randint
from typing import Annotated
from urllib import response

from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import AzureCliCredential, DefaultAzureCredential
from pydantic import Field
import os
from azure.ai.evaluation import ToolCallAccuracyEvaluator, AzureOpenAIModelConfiguration
from azure.ai.evaluation import IntentResolutionEvaluator, TaskAdherenceEvaluator, ResponseCompletenessEvaluator
from pprint import pprint
from agent_framework.observability import get_tracer, setup_observability
from opentelemetry.trace import SpanKind
from opentelemetry.trace.span import format_trace_id

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_KEY"],
    api_version="2024-02-15-preview",  # Compatible API version for evaluators
    azure_deployment="gpt-4.1",  # Match the deployment used in the agent
)


tool_call_accuracy = ToolCallAccuracyEvaluator(model_config=model_config)

async def main() -> None:
    print("=== Azure AI Chat Client with Existing Agent ===")
    setup_observability()

    # Create the client
    async with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"], credential=credential) as client,
    ):
        deployment = "gpt-4.1"
        chat_client = AzureAIAgentClient(credential=credential, 
                            project_client=client,
                            model_deployment_name=deployment
                            )
        # await chat_client.setup_azure_ai_observability()
        # with get_tracer().start_as_current_span("IndAgentEvalRealtime", kind=SpanKind.CLIENT) as current_span:
        #         print(f"Trace ID: {format_trace_id(current_span.get_span_context().trace_id)}")
        myAgent = "IntentAgent"
        # Create an agent that will persist
        # created_agent = await client.agents.create(
        #     model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"], name="TestEvalAgent"
        # )
        created_agent = await client.agents.get(agent_name=myAgent)
        query = "What's the weather like in Tokyo?"
        try:
            openai_client = client.get_openai_client()

            # Reference the agent to get a response
            response = await openai_client.responses.create(
                input=[{"role": "user", "content": "Summarize the RFP for virginia Railway Express project?"}],
                extra_body={"agent": {"name": created_agent.name, "type": "agent_reference"}},
            )

            print("Initial Response Status:", response.status)
            print("Response ID:", response.id)
            print("\n" + "="*80 + "\n")
            result = str(response)

            # query = "How is the weather in Seattle ?"
            tool_call = {
                "type": "tool_call",
                "tool_call_id": "call_CUdbkBfvVBla2YP3p24uhElJ",
                "name": "fetch_weather",
                "arguments": {"location": "Seattle"},
            }

            tool_definition = {
                "id": "fetch_weather",
                "name": "fetch_weather",
                "description": "Fetches the weather information for the specified location.",
                "parameters": {
                    "type": "object",
                    "properties": {"location": {"type": "string", "description": "The location to fetch weather for."}},
                },
            }
            response = tool_call_accuracy(query=query, tool_calls=tool_call, tool_definitions=tool_definition)
            pprint(response)
            response_completeness_evaluator = ResponseCompletenessEvaluator(model_config=model_config)
            result = response_completeness_evaluator(
                response=result,
                ground_truth=result,
            )
            pprint(result)
            intent_resolution_evaluator = IntentResolutionEvaluator(model_config)
            # Success example. Intent is identified and understood and the response correctly resolves user intent
            result = intent_resolution_evaluator(
                query=query,
                response=result,
            )
            pprint(result)
            task_adherence_evaluator = TaskAdherenceEvaluator(model_config)
            result = task_adherence_evaluator(
                query=query,
                response=result,
            )
            pprint(result)
        finally:
            # Clean up the agent manually
            pass
            
            # await client.agents.delete_agent(created_agent.id)


if __name__ == "__main__":
    asyncio.run(main())