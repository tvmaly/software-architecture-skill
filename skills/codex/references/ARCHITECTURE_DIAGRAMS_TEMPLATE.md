# Architecture Diagrams

> Diagrams should be small, readable, and grounded in repository evidence. Prefer several simple diagrams over one large diagram.

## Diagram Guidance

Include Mermaid diagrams only when they clarify the repository.

A diagram may be omitted when the repository is very small, such as a single script under roughly 200 lines, and the diagram would add more noise than value.

## 1. System Context

Use this diagram to show how the repository interacts with users, systems, databases, queues, files, and external services.

```mermaid
flowchart LR
    User[User or Scheduler] --> Repo[This Repository]
    Repo --> DB[(Database)]
    Repo --> External[External System]
```

Explain the diagram in 2-5 sentences and cite the files or configs that support it.

## 2. Component or Module View

Use this diagram to show major packages, apps, or modules and their responsibilities.

```mermaid
flowchart TB
    Entry[Entry Points] --> Domain[Domain Logic]
    Domain --> Data[Data Access]
    Domain --> Integrations[Integrations]
    Tests[Tests] -. verify .-> Domain
```

Explain the most important dependency direction.

## 3. Request, Job, or Data Flow

Use this diagram to show the most important runtime path.

```mermaid
sequenceDiagram
    participant Caller
    participant EntryPoint
    participant Service
    participant DataStore
    Caller->>EntryPoint: request/command/job trigger
    EntryPoint->>Service: validate and coordinate
    Service->>DataStore: read/write
    DataStore-->>Service: results
    Service-->>EntryPoint: response/output
    EntryPoint-->>Caller: result
```

Explain the main flow and where errors are handled if visible.

## 4. Dependency Direction

Use this when dependency boundaries matter.

```mermaid
flowchart LR
    UI[UI Layer] --> API[API Layer]
    API --> Domain[Domain Layer]
    Domain --> Repository[Repository/Data Access Layer]
    Repository --> DB[(Database)]
```

Explain whether the current dependency direction appears clean, mixed, or unclear.

## 5. Boundary and Contract View

Use this when component boundaries, schemas, or public interfaces are important to safe changes.

```mermaid
flowchart LR
    Caller[Caller or Workflow] --> Contract[Public Contract]
    Contract --> Component[Owning Component]
    Component --> Adapter[Boundary Adapter]
    Adapter --> External[(External System or Store)]
```

Explain what the contract is, which component owns it, and which files provide evidence. If contracts are implicit or missing, say that directly.

## 6. AI-Agent Navigation View

Use this when future agents need a concise reading path before editing.

```mermaid
flowchart TB
    Context[Context Docs] --> Entry[Entry Points]
    Entry --> Core[Core Logic]
    Core --> Tests[Focused Tests]
    Core --> Contracts[Contracts or Schemas]
    Core --> Runtime[Runtime Config]
```

Explain the safest reading order and the verification path. Keep this diagram focused on navigation, not every file in the repository.

## 7. Runtime and Deployment View

Use this when deployment, runtime, or operations are visible in the repo.

```mermaid
flowchart LR
    CI[CI/CD] --> Build[Build Artifact]
    Build --> Runtime[Runtime Environment]
    Runtime --> Logs[Logs/Monitoring]
    Runtime --> Config[Configuration]
```

Explain what is known and what requires human validation.
