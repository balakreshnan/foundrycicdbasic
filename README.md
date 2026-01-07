# Microsoft Agent Framework with Microsoft Foundry CI/CD

Agent framework and Microsoft Foundry CI/CD using basic

## Prerequisites

- Azure subscription. If you don't have one, create a free account before you begin.
- Azure DevOps organization. If you don't have one, create a free organization before you begin.
- Microsoft Foundry CI/CD access. If you don't have access, contact your Microsoft representative.
- python 3.13+ installed locally.
- An Azure AI Project resource with the Agent feature enabled. You can create this resource via the Azure Portal or Azure CLI.

## Setup

1. First Create Agent and Deploy
2. Use the existing agent, Evaluate Agent, Red Teaming

## Architecture flow

![Architecture](./images/deploymentflow.jpg)

## Step 1: Create Agent and Deploy

- createagent.py: Creates a basic weather agent using the Azure AI Project SDK and deploys it to the Azure AI Project resource.
- Execute createagent.py only once.

## Step 2: Use the existing agent build application, Evaluate Agent, Red Teaming and Deploy

- exagent.py: Uses an existing agent created in the previous step to answer a weather-related question.
- agenteval.py: Evaluates the performance of the existing agent in real-time using the Azure
- Redteam.py: Performs red teaming on the existing agent to test its robustness against adversarial prompts.

------------------------------------------
| exagent.py → agenteval.py → redteam.py |
------------------------------------------

https://medium.com/gopenai/microsoft-foundry-agent-ops-agentops-9bb9304d2a0c

### Azure DevOps Pipeline

https://github.com/balakreshnan/foundrycicdbasic/blob/main/cicd/README.md

### Github Actions

https://github.com/balakreshnan/foundrycicdbasic/blob/main/.github/workflows/README.md

## Conclusion

- This is a basic example of how to create, deploy, use, evaluate, and red team an agent using the Microsoft Agent Framework and Microsoft Foundry CI/CD.
- Usually the agent creation will be more complex and involve more sophisticated logic and integrations.
- Agent creation will be separate deployment.
- Agent usage or consumption will be part of application that is consuming the agent.
