# foundrycicdbasic

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

## Creae Agent and Deploy

- createagent.py: Creates a basic weather agent using the Azure AI Project SDK and deploys it to the Azure AI Project resource.

## Use the existing agent build application, Evaluate Agent, Red Teaming and Deploy

- exagent.py: Uses an existing agent created in the previous step to answer a weather-related question.
- agenteval.py: Evaluates the performance of the existing agent in real-time using the Azure
- Redteam.py: Performs red teaming on the existing agent to test its robustness against adversarial prompts.