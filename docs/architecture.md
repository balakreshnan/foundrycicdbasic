# Architecture Overview

## 📋 System Architecture

This document provides a comprehensive overview of the Microsoft Agent Framework with Foundry CI/CD architecture, including system components, deployment flows, and agent reusability patterns.

## 🏗️ High-Level System Architecture

```mermaid
graph TB
    subgraph "Development"
        A[Developer] --> B[Code Repository]
        B --> C[Local Testing]
    end
    
    subgraph "CI/CD Platform"
        D[Azure DevOps / GitHub Actions]
        E[Build Pipeline]
        F[Test Pipeline]
        G[Deploy Pipeline]
    end
    
    subgraph "Azure Infrastructure"
        H[Dev Environment]
        I[Test Environment]
        J[Prod Environment]
    end
    
    subgraph "Azure AI Foundry - Dev"
        H --> K[AI Agent Service]
        K --> L[OpenAI Service]
        K --> M[Observability]
    end
    
    subgraph "Azure AI Foundry - Test"
        I --> N[AI Agent Service]
        N --> O[OpenAI Service]
        N --> P[Evaluation Service]
        N --> Q[Red Team Service]
    end
    
    subgraph "Azure AI Foundry - Prod"
        J --> R[AI Agent Service]
        R --> S[OpenAI Service]
        R --> T[Monitoring]
    end
    
    subgraph "Consumer Applications"
        U[Web App]
        V[Mobile App]
        W[API Services]
    end
    
    B --> D
    D --> E
    E --> F
    F --> G
    G --> H
    G --> I
    G --> J
    
    R --> U
    R --> V
    R --> W
    
    style D fill:#e1f5ff
    style K fill:#c8e6c9
    style N fill:#fff9c4
    style R fill:#ffcdd2
```

## 🔄 Agent Creation Deployment Flow

This diagram shows the complete flow for creating and deploying a new AI agent across environments.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Git as Git Repository
    participant CI as CI/CD Pipeline
    participant Build as Build Stage
    participant DevEnv as Dev Environment
    participant TestEnv as Test Environment
    participant Approver as Approver
    participant ProdEnv as Production
    
    Dev->>Git: 1. Commit createagent.py
    Note over Dev,Git: Changes to agent configuration
    
    Git->>CI: 2. Trigger Pipeline
    Note over Git,CI: On push to main/develop
    
    CI->>Build: 3. Start Build Stage
    Build->>Build: 4. Install dependencies
    Build->>Build: 5. Validate Python syntax
    Build->>Build: 6. Create artifacts
    Note over Build: Build artifact contains<br/>createagent.py + requirements.txt
    
    Build->>DevEnv: 7. Deploy to Dev
    DevEnv->>DevEnv: 8. Authenticate with Azure
    DevEnv->>DevEnv: 9. Setup observability
    DevEnv->>DevEnv: 10. Create/Update agent
    DevEnv->>DevEnv: 11. Test agent execution
    DevEnv-->>Build: 12. Deployment Success
    
    Build->>TestEnv: 13. Deploy to Test
    TestEnv->>TestEnv: 14. Authenticate with Azure
    TestEnv->>TestEnv: 15. Create/Update agent
    TestEnv->>TestEnv: 16. Test agent execution
    TestEnv-->>Build: 17. Deployment Success
    
    Build->>Approver: 18. Request Production Approval
    Note over Build,Approver: Manual approval gate
    Approver->>Approver: 19. Review test results
    Approver->>Build: 20. Approve Deployment
    
    Build->>ProdEnv: 21. Deploy to Production
    ProdEnv->>ProdEnv: 22. Authenticate with Azure
    ProdEnv->>ProdEnv: 23. Create/Update agent
    ProdEnv->>ProdEnv: 24. Test agent execution
    ProdEnv-->>Build: 25. Deployment Success
    
    Build->>Dev: 26. Notify Completion
    Note over Dev: Agent available in all environments
```

## 🧪 Agent Consumption and Testing Flow

This diagram illustrates how existing agents are tested, evaluated, and security-scanned.

```mermaid
sequenceDiagram
    participant CI as CI/CD Pipeline
    participant Dev as Dev Environment
    participant Agent as AI Agent
    participant Test as Test Environment
    participant Eval as Evaluation Service
    participant RedTeam as Red Team Service
    participant Storage as Artifact Storage
    participant Prod as Production
    
    CI->>Dev: 1. Test Existing Agent (exagent.py)
    Dev->>Agent: 2. Retrieve agent by name
    Agent-->>Dev: 3. Agent instance
    Dev->>Agent: 4. Send test query
    Agent->>Agent: 5. Process query
    Note over Agent: May require MCP approvals
    Agent-->>Dev: 6. Return response with citations
    Dev-->>CI: 7. Test results
    
    CI->>Test: 8. Run Agent Evaluation (agenteval.py)
    Test->>Agent: 9. Get agent instance
    Test->>Agent: 10. Send evaluation query
    Agent-->>Test: 11. Agent response
    
    Test->>Eval: 12. Evaluate tool call accuracy
    Eval-->>Test: 13. Tool accuracy score
    
    Test->>Eval: 14. Evaluate response completeness
    Eval-->>Test: 15. Completeness score
    
    Test->>Eval: 16. Evaluate intent resolution
    Eval-->>Test: 17. Intent score
    
    Test->>Eval: 18. Evaluate task adherence
    Eval-->>Test: 19. Adherence score
    
    Test-->>CI: 20. Evaluation results
    
    CI->>Test: 21. Run Red Team Testing (redteam.py)
    Test->>RedTeam: 22. Initialize red team scan
    
    loop For each attack strategy
        RedTeam->>RedTeam: 23. Generate adversarial prompt
        RedTeam->>Agent: 24. Send attack prompt
        Agent-->>RedTeam: 25. Agent response
        RedTeam->>RedTeam: 26. Evaluate safety
    end
    
    RedTeam-->>Test: 27. Security scorecard
    Test->>Storage: 28. Save security results (JSON)
    Test-->>CI: 29. Red team results
    
    CI->>CI: 30. Check quality thresholds
    
    alt Quality Gates Passed
        CI->>Prod: 31. Verify Production Agent
        Prod->>Agent: 32. Quick health check
        Agent-->>Prod: 33. Health OK
        Prod-->>CI: 34. Verification success
        CI->>CI: 35. Mark deployment successful
    else Quality Gates Failed
        CI->>CI: 36. Fail pipeline
        CI->>Dev: 37. Notify failure
    end
```

## 🔁 Agent Reusability Pattern

This diagram shows how agents created in one deployment can be consumed by multiple applications.

```mermaid
graph TB
    subgraph "Agent Creation Deployment"
        A[createagent.py] --> B[Azure AI Foundry]
        B --> C[Agent: cicdagenttest]
        C --> D[Agent Registry]
    end
    
    subgraph "Agent Consumption Applications"
        D --> E[Web Application 1]
        D --> F[Mobile App]
        D --> G[Backend API Service]
        D --> H[Chatbot Interface]
        D --> I[CLI Tool]
    end
    
    subgraph "Each Consumer Uses exagent.py Pattern"
        E --> J[Get Agent by Name]
        F --> J
        G --> J
        H --> J
        I --> J
        
        J --> K[Send Queries]
        K --> L[Process Responses]
        L --> M[Handle MCP Approvals]
        M --> N[Display Results]
    end
    
    style A fill:#e1f5ff
    style C fill:#c8e6c9
    style D fill:#fff9c4
    style J fill:#ffcdd2
```

### Agent Reusability Benefits

```mermaid
graph LR
    A[Single Agent Deployment] --> B[Multiple Consumers]
    B --> C[Consistent Behavior]
    B --> D[Centralized Updates]
    B --> E[Reduced Costs]
    B --> F[Easier Maintenance]
    
    C --> G[Same responses across apps]
    D --> H[Update once, affects all]
    E --> I[No duplicate agents]
    F --> J[Single point of control]
    
    style A fill:#c8e6c9
    style B fill:#fff9c4
```

## 📊 Deployment Flow Diagram

### Create Agent Deployment Process

```mermaid
flowchart TD
    Start([Developer commits code]) --> Trigger{Pipeline<br/>Triggered?}
    
    Trigger -->|Yes| Build[Build Stage]
    Trigger -->|No| End1([No Action])
    
    Build --> Validate{Syntax<br/>Valid?}
    Validate -->|No| Fail1([Build Failed])
    Validate -->|Yes| Artifacts[Create Artifacts]
    
    Artifacts --> DeployDev[Deploy to Dev]
    DeployDev --> TestDev{Dev Tests<br/>Pass?}
    TestDev -->|No| Fail2([Dev Failed])
    TestDev -->|Yes| DeployTest[Deploy to Test]
    
    DeployTest --> TestTest{Test Tests<br/>Pass?}
    TestTest -->|No| Fail3([Test Failed])
    TestTest -->|Yes| Approval{Production<br/>Approval?}
    
    Approval -->|Rejected| Cancel([Deployment Cancelled])
    Approval -->|Timeout| Timeout([Approval Timeout])
    Approval -->|Approved| DeployProd[Deploy to Production]
    
    DeployProd --> TestProd{Prod Tests<br/>Pass?}
    TestProd -->|No| Rollback([Rollback Required])
    TestProd -->|Yes| Success([Deployment Complete])
    
    style Build fill:#e1f5ff
    style DeployDev fill:#c8e6c9
    style DeployTest fill:#fff9c4
    style DeployProd fill:#ffcdd2
    style Success fill:#a5d6a7
    style Fail1 fill:#ef9a9a
    style Fail2 fill:#ef9a9a
    style Fail3 fill:#ef9a9a
    style Rollback fill:#ef9a9a
```

### Agent Testing and Evaluation Process

```mermaid
flowchart TD
    Start([Pipeline Triggered]) --> Build[Build & Validate Scripts]
    Build --> DevTest[Test with exagent.py in Dev]
    
    DevTest --> DevOK{Dev Test<br/>Successful?}
    DevOK -->|No| FailDev([Dev Test Failed])
    DevOK -->|Yes| Eval[Run agenteval.py in Test]
    
    Eval --> EvalMetrics[Collect Evaluation Metrics]
    EvalMetrics --> CheckScores{Scores Above<br/>Threshold?}
    
    CheckScores -->|No| FailEval([Evaluation Failed])
    CheckScores -->|Yes| RedTeam[Run redteam.py in Test]
    
    RedTeam --> SecurityScan[Security Attack Testing]
    SecurityScan --> Scorecard[Generate Security Scorecard]
    Scorecard --> SaveArtifacts[Save Results as Artifacts]
    
    SaveArtifacts --> CheckSecurity{Security<br/>Pass Rate OK?}
    CheckSecurity -->|No| FailSec([Security Failed])
    CheckSecurity -->|Yes| ProdVerify[Verify Production Agent]
    
    ProdVerify --> VerifyOK{Verification<br/>Successful?}
    VerifyOK -->|No| FailProd([Prod Verification Failed])
    VerifyOK -->|Yes| Success([All Tests Passed])
    
    style Build fill:#e1f5ff
    style DevTest fill:#c8e6c9
    style Eval fill:#fff9c4
    style RedTeam fill:#ffcdd2
    style Success fill:#a5d6a7
    style FailDev fill:#ef9a9a
    style FailEval fill:#ef9a9a
    style FailSec fill:#ef9a9a
    style FailProd fill:#ef9a9a
```

## 🎯 Component Architecture

### Core Components

```mermaid
graph TB
    subgraph "Python Scripts"
        A[createagent.py]
        B[exagent.py]
        C[agenteval.py]
        D[redteam.py]
    end
    
    subgraph "Agent Framework"
        E[AzureAIClient]
        F[AIProjectClient]
        G[Observability]
    end
    
    subgraph "Azure Services"
        H[Azure AI Foundry]
        I[Azure OpenAI]
        J[Azure Monitor]
        K[Azure Key Vault]
    end
    
    subgraph "Evaluation Framework"
        L[ToolCallAccuracyEvaluator]
        M[IntentResolutionEvaluator]
        N[TaskAdherenceEvaluator]
        O[ResponseCompletenessEvaluator]
        P[RedTeam Framework]
    end
    
    A --> E
    B --> F
    C --> F
    D --> F
    
    E --> H
    F --> H
    E --> I
    F --> I
    
    G --> J
    E --> K
    F --> K
    
    C --> L
    C --> M
    C --> N
    C --> O
    D --> P
    
    P --> I
    L --> I
    M --> I
    N --> I
    O --> I
    
    style A fill:#e1f5ff
    style B fill:#c8e6c9
    style C fill:#fff9c4
    style D fill:#ffcdd2
```

## 🔐 Security Architecture

```mermaid
graph TB
    subgraph "Authentication Layer"
        A[DefaultAzureCredential]
        B[Service Principal]
        C[Managed Identity]
        D[Azure CLI]
    end
    
    subgraph "Secret Management"
        E[Azure Key Vault]
        F[GitHub Secrets]
        G[Azure DevOps Variables]
    end
    
    subgraph "Application Layer"
        H[Agent Scripts]
        I[CI/CD Pipelines]
    end
    
    subgraph "Azure Resources"
        J[Azure AI Foundry]
        K[Azure OpenAI]
        L[Azure Monitor]
    end
    
    A --> B
    A --> C
    A --> D
    
    E --> H
    F --> I
    G --> I
    
    H --> A
    I --> A
    
    A --> J
    A --> K
    A --> L
    
    style A fill:#e1f5ff
    style E fill:#c8e6c9
    style J fill:#fff9c4
```

## 📈 Data Flow Architecture

### Agent Creation Data Flow

```mermaid
flowchart LR
    A[Environment Variables] --> B[createagent.py]
    B --> C[Azure Authentication]
    C --> D[AzureAIClient]
    D --> E[Create Agent Request]
    E --> F[Azure AI Foundry API]
    F --> G[Agent Instance]
    G --> H[Execute Test Query]
    H --> I[Agent Response]
    I --> J[OpenTelemetry Trace]
    J --> K[Azure Monitor]
    
    style B fill:#e1f5ff
    style G fill:#c8e6c9
    style K fill:#fff9c4
```

### Agent Consumption Data Flow

```mermaid
flowchart LR
    A[User Query] --> B[exagent.py]
    B --> C[Get Agent by Name]
    C --> D[Azure AI Foundry]
    D --> E[Agent Instance]
    E --> F[OpenAI Client]
    F --> G[Send Query]
    G --> H{MCP Approval<br/>Required?}
    
    H -->|Yes| I[Detect MCP Requests]
    I --> J[Auto-Approve]
    J --> K[Poll for Completion]
    K --> L[Get Final Response]
    
    H -->|No| L
    
    L --> M[Extract Text & Citations]
    M --> N[Format Output]
    N --> O[Display to User]
    
    style B fill:#e1f5ff
    style E fill:#c8e6c9
    style M fill:#fff9c4
```

## 🌐 Multi-Environment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        A1[Dev Azure AI Project]
        A2[Dev OpenAI Service]
        A3[Dev Agents]
        A1 --- A2
        A1 --- A3
    end
    
    subgraph "Test Environment"
        B1[Test Azure AI Project]
        B2[Test OpenAI Service]
        B3[Test Agents]
        B4[Evaluation Service]
        B5[Red Team Service]
        B1 --- B2
        B1 --- B3
        B1 --- B4
        B1 --- B5
    end
    
    subgraph "Production Environment"
        C1[Prod Azure AI Project]
        C2[Prod OpenAI Service]
        C3[Prod Agents]
        C4[Application Insights]
        C5[Consumer Apps]
        C1 --- C2
        C1 --- C3
        C1 --- C4
        C3 --- C5
    end
    
    subgraph "CI/CD Pipeline"
        D[Build] --> E[Dev Deploy]
        E --> F[Test Deploy]
        F --> G{Approval}
        G --> H[Prod Deploy]
    end
    
    E -.-> A1
    F -.-> B1
    H -.-> C1
    
    style A1 fill:#c8e6c9
    style B1 fill:#fff9c4
    style C1 fill:#ffcdd2
    style D fill:#e1f5ff
```

## 🔄 Agent Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Development: Create agent code
    Development --> Build: Commit & push
    Build --> Validation: Run syntax checks
    Validation --> Failed: Validation errors
    Validation --> DevDeploy: Validation passed
    
    DevDeploy --> DevTest: Deploy to dev
    DevTest --> TestDeploy: Dev tests passed
    DevTest --> Failed: Dev tests failed
    
    TestDeploy --> Evaluation: Deploy to test
    Evaluation --> SecurityScan: Metrics acceptable
    Evaluation --> Failed: Metrics below threshold
    
    SecurityScan --> Approval: Security passed
    SecurityScan --> Failed: Security issues found
    
    Approval --> ProdDeploy: Approved
    Approval --> Cancelled: Rejected
    
    ProdDeploy --> Active: Deployment successful
    ProdDeploy --> Failed: Deployment failed
    
    Active --> Monitoring: Monitor usage
    Monitoring --> Active: Healthy
    Monitoring --> Investigation: Issues detected
    
    Investigation --> Update: Fix required
    Investigation --> Active: False alarm
    
    Update --> Development: Create fixes
    
    Failed --> Investigation: Analyze failure
    Cancelled --> [*]
    
    Active --> Deprecated: New version deployed
    Deprecated --> Retired: Grace period ended
    Retired --> [*]
```

## 📊 Observability Architecture

```mermaid
graph TB
    subgraph "Application Layer"
        A[Agent Scripts]
        B[Python Code]
    end
    
    subgraph "Observability Framework"
        C[OpenTelemetry SDK]
        D[Tracer]
        E[Meter]
        F[Logger]
    end
    
    subgraph "Telemetry Data"
        G[Traces]
        H[Metrics]
        I[Logs]
    end
    
    subgraph "Azure Monitor"
        J[Application Insights]
        K[Log Analytics]
        L[Dashboards]
        M[Alerts]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    C --> F
    
    D --> G
    E --> H
    F --> I
    
    G --> J
    H --> J
    I --> K
    
    J --> L
    K --> L
    L --> M
    
    style A fill:#e1f5ff
    style C fill:#c8e6c9
    style J fill:#fff9c4
```

## 🎯 Key Architectural Principles

### 1. Separation of Concerns

- **Agent Creation**: Isolated in `createagent.py`
- **Agent Consumption**: Handled by `exagent.py`
- **Evaluation**: Dedicated `agenteval.py`
- **Security Testing**: Separate `redteam.py`

### 2. Environment Isolation

- Independent Azure resources per environment
- Separate credentials and configurations
- No cross-environment dependencies
- Progressive deployment: Dev → Test → Prod

### 3. Reusability

- Agents created once, consumed many times
- Consistent agent behavior across applications
- Centralized updates and maintenance
- Shared evaluation and security testing

### 4. Security by Design

- Multiple authentication methods
- Secrets stored in Key Vault
- Role-based access control (RBAC)
- Approval gates for production
- Regular security scanning

### 5. Observability First

- Distributed tracing with OpenTelemetry
- Trace IDs for request correlation
- Metrics collection and monitoring
- Centralized logging in Azure Monitor

### 6. CI/CD Integration

- Automated build and validation
- Multi-environment deployment
- Quality gates and thresholds
- Automated testing and security scans

## 📚 Architecture Decision Records (ADRs)

### ADR-001: Use DefaultAzureCredential for Authentication

**Status**: Accepted

**Context**: Need flexible authentication for local dev and CI/CD

**Decision**: Use `DefaultAzureCredential` which tries multiple methods

**Consequences**: 
- ✅ Works in multiple environments without code changes
- ✅ Supports service principal, managed identity, Azure CLI
- ⚠️ Requires understanding of credential chain order

### ADR-002: Separate Agent Creation and Consumption

**Status**: Accepted

**Context**: Need clear separation between deployment and usage

**Decision**: Create separate scripts for creation (`createagent.py`) and consumption (`exagent.py`)

**Consequences**:
- ✅ Clear responsibilities
- ✅ Enables agent reusability
- ✅ Different deployment patterns
- ⚠️ Requires understanding of both patterns

### ADR-003: Multi-Environment Deployment with Approval Gates

**Status**: Accepted

**Context**: Need safe path to production with validation

**Decision**: Deploy through Dev → Test → Prod with approvals

**Consequences**:
- ✅ Gradual rollout reduces risk
- ✅ Testing in non-prod before prod
- ✅ Manual approval for production
- ⚠️ Longer deployment time

### ADR-004: Include Security Testing in Pipeline

**Status**: Accepted

**Context**: Need to ensure agents are safe before production

**Decision**: Integrate red team testing in test environment

**Consequences**:
- ✅ Automated security validation
- ✅ Identifies vulnerabilities early
- ✅ Security reports as artifacts
- ⚠️ Increases pipeline execution time

## 🔗 Related Documentation

- [createagent.py](./createagent.md) - Agent creation details
- [exagent.py](./exagent.md) - Agent consumption details
- [agenteval.py](./agenteval.md) - Evaluation metrics
- [redteam.py](./redteam.md) - Security testing
- [Deployment Guide](./deployment.md) - Deployment procedures
- [Main Documentation](./README.md) - Documentation index

---

**Last Updated**: December 2025  
**Version**: 1.0  
**Maintained by**: Architecture & DevOps Teams
