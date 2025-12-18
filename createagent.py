import re
from azure.identity import DefaultAzureCredential
#from azure.ai.projects import AIProjectClient
from agent_framework.azure import AzureAIClient
from agent_framework.observability import get_tracer, setup_observability
import os
from dotenv import load_dotenv
from opentelemetry.trace import SpanKind
from opentelemetry.trace.span import format_trace_id

# Load environment variables
load_dotenv()

myEndpoint = os.getenv("AZURE_AI_PROJECT")

async def createagent():
    setup_observability()
    credential = DefaultAzureCredential()

    myAgent = "cicdagenttest"
    with get_tracer().start_as_current_span("cicdagenttest", kind=SpanKind.CLIENT) as current_span:
        print(f"Trace ID: {format_trace_id(current_span.get_span_context().trace_id)}")
        # Create a new agent
        # Since no Agent ID is provided, the agent will be automatically created.
        # For authentication, run `az login` command in terminal or replace AzureCliCredential with preferred
        # authentication option.
        # Create client and agent without async with
        credential = DefaultAzureCredential()
        client = AzureAIClient(credential=credential)

        # Create agent (doesn't return a context manager)
        agent = client.create_agent(
            name=myAgent, 
            instructions="You are CICD Agent, an AI agent designed to assist with continuous integration and continuous deployment tasks."
        )

        # Run the agent
        result = await agent.run("Create a CICD pipeline for a Python application using GitHub Actions.")
        print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(createagent())