# Before running the sample:
#    pip install --pre azure-ai-projects>=2.0.0b1
#    pip install azure-identity

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



def existingagent():
    setup_observability()
    project_client = AIProjectClient(
        endpoint=myEndpoint,
        credential=DefaultAzureCredential(),
    )

    def extract_response_text(raw):
        raw = str(raw)   # <-- ensure it's always a string
        m = re.search(r"ResponseOutputText\(.*?text='([^']+)'", raw, re.DOTALL)
        return m.group(1) if m else None


    myAgent = "rfpagent"
    with get_tracer().start_as_current_span("ExistingAgent", kind=SpanKind.CLIENT) as current_span:
        print(f"Trace ID: {format_trace_id(current_span.get_span_context().trace_id)}")
        # Get an existing agent
        agent = project_client.agents.get(agent_name=myAgent)
        print(f"Retrieved agent: {agent.name}")

        openai_client = project_client.get_openai_client()

        # Reference the agent to get a response
        response = openai_client.responses.create(
            input=[{"role": "user", "content": "Summarize the RFP for virginia Railway Express project?"}],
            extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
        )

        print("Initial Response Status:", response.status)
        print("Response ID:", response.id)
        print("\n" + "="*80 + "\n")

        # Check if there are MCP approval requests
        mcp_approval_requests = []
        for output_item in response.output:
            if hasattr(output_item, 'type') and output_item.type == 'mcp_approval_request':
                mcp_approval_requests.append(output_item)
                print(f"MCP Approval Request Found:")
                print(f"  - ID: {output_item.id}")
                print(f"  - Tool: {output_item.name}")
                print(f"  - Server: {output_item.server_label}")
                print(f"  - Arguments: {output_item.arguments}")
                print()

        # Auto-approve all MCP tool calls
        if mcp_approval_requests:
            print(f"Auto-approving {len(mcp_approval_requests)} MCP tool call(s)...\n")
            
            # Approve each MCP request by creating a new response with approval
            for approval_request in mcp_approval_requests:
                response = openai_client.responses.create(
                    previous_response_id=response.id,
                    input=[{
                        "type": "mcp_approval_response",
                        "approve": True,
                        "approval_request_id": approval_request.id
                    }],
                    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}}
                )
                print(f"✓ Approved: {approval_request.name}")
            
            print("\n" + "="*80 + "\n")
            print("Waiting for final response...\n")
            
            # Poll for the final result
            import time
            max_retries = 30
            retry_count = 0
            
            while retry_count < max_retries:
                response = openai_client.responses.retrieve(response_id=response.id)
                
                if response.status == 'completed':
                    print("Response completed!")
                    # print('Result:', response)
                    break
                elif response.status == 'failed':
                    print("Response failed!")
                    if response.error:
                        print(f"Error: {response.error}")
                    break
                else:
                    print(f"Status: {response.status} - waiting...")
                    time.sleep(2)
                    retry_count += 1
            
            print("\n" + "="*80 + "\n")

        # Display the final result with citations
        print("FINAL RESPONSE:")
        print("="*80)

        for output_item in response.output:
            item_type = getattr(output_item, 'type', None)
            
            # Check for message output (ResponseOutputMessage)
            if item_type == 'message':
                print("\n📄 Response Text:")
                if hasattr(output_item, 'content') and output_item.content:
                    for content_item in output_item.content:
                        if hasattr(content_item, 'text'):
                            print(content_item.text)
                            print()
                            
                            # Display citations if available
                            if hasattr(content_item, 'annotations') and content_item.annotations:
                                print("\n📚 Citations:")
                                for i, annotation in enumerate(content_item.annotations, 1):
                                    print(f"\n  [{i}] {annotation.text if hasattr(annotation, 'text') else 'Citation'}")
                                    if hasattr(annotation, 'file_citation'):
                                        citation = annotation.file_citation
                                        print(f"      Source: {citation.file_name if hasattr(citation, 'file_name') else 'N/A'}")
                                        if hasattr(citation, 'quote'):
                                            print(f"      Quote: {citation.quote}")
            
            # Check for direct text output (older format)
            elif item_type == 'response_output_text':
                print("\n📄 Response Text:")
                print(output_item.text)
                print()
                
                # Display citations if available
                if hasattr(output_item, 'annotations') and output_item.annotations:
                    print("\n📚 Citations:")
                    for i, annotation in enumerate(output_item.annotations, 1):
                        print(f"\n  [{i}] {annotation.text if hasattr(annotation, 'text') else 'Citation'}")
                        if hasattr(annotation, 'file_citation'):
                            citation = annotation.file_citation
                            print(f"      Source: {citation.file_name if hasattr(citation, 'file_name') else 'N/A'}")
                            if hasattr(citation, 'quote'):
                                print(f"      Quote: {citation.quote}")
            
            # Check for MCP call results
            elif item_type == 'mcp_call':
                print("\n🔧 MCP Tool Call:")
                print(f"  Tool: {output_item.name}")
                print(f"  Status: {output_item.status}")
                if hasattr(output_item, 'output') and output_item.output:
                    # Limit output display to avoid clutter
                    output_text = str(output_item.output)
                    if len(output_text) > 500:
                        print(f"  Output: {output_text[:500]}... (truncated)")
                    else:
                        print(f"  Output: {output_text}")
                print()

        print("\n" + "="*80)
    print("End of conversation with agent.")

if __name__ == "__main__":
    existingagent()