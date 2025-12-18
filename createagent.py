import re
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from agent_framework.observability import get_tracer, setup_observability
import os
from dotenv import load_dotenv
from opentelemetry.trace import SpanKind
from opentelemetry.trace.span import format_trace_id

# Load environment variables
load_dotenv()

myEndpoint = os.getenv("AZURE_AI_PROJECT")

def createagent():
    setup_observability()
    project_client = AIProjectClient(
        endpoint=myEndpoint,
        credential=DefaultAzureCredential(),
    )

    myAgent = "rfpagent"
    with get_tracer().start_as_current_span("CreateAgent", kind=SpanKind.CLIENT) as current_span:
        print(f"Trace ID: {format_trace_id(current_span.get_span_context().trace_id)}")
        # Create a new agent
        agent = project_client.agents.create(
            agent_name=myAgent,
            description="An agent to assist with RFP analysis and summarization.",
            instructions="""
            You are an expert assistant specialized in analyzing and summarizing Requests for Proposals (RFPs).
            Your tasks include:
            - Extracting key information from RFP documents.
            - Summarizing the main points and requirements.
            - Providing insights on how to respond effectively to RFPs.
            Boundaries:
            - Do not provide legal or financial advice.
            - Always ensure confidentiality of sensitive information.
            """,
            tools=[
                {
                    "name": "RFPAnalyzer",
                    "type": "custom_tool",
                    "description": "A tool to analyze RFP documents and extract relevant information.",
                }
            ],
        )
        print(f"Created agent: {agent.name} with ID: {agent.id}")

if __name__ == "__main__":
    createagent()