# Visual Project Overview

Визуализация проекта с разных точек зрения.

## Оглавление

1. [Архитектура системы](#архитектура-системы)
2. [Поток данных](#поток-данных)
3. [Граф зависимостей](#граф-зависимостей)
4. [Последовательность взаимодействий](#последовательность-взаимодействий)
5. [Жизненный цикл сообщения](#жизненный-цикл-сообщения)
6. [Структура хранения](#структура-хранения)
7. [Обработка ошибок](#обработка-ошибок)
8. [Структура проекта](#структура-проекта)
9. [Timeline разработки](#timeline-разработки)
10. [Makefile команды](#makefile-команды)

---

## Архитектура системы

### High-Level архитектура

```mermaid
graph TB
    subgraph External["🌐 External Services"]
        TG[Telegram API]
        OR[Openrouter API]
    end

    subgraph App["🤖 Application"]
        Main[main.py<br/>Entry Point]
        Bot[bot.py<br/>Aiogram Bot]
        Handler[handler.py<br/>Message Handler]
        LLM[llm_client.py<br/>LLM Client]
        DM[dialog_manager.py<br/>Dialog Manager]
        Config[config.py<br/>Configuration]
    end

    subgraph Storage["💾 Storage"]
        Memory[In-Memory Dict<br/>user_id → messages]
        Logs[logs/<br/>JSON Logs]
    end

    subgraph Resources["📁 Resources"]
        ENV[.env<br/>Secrets]
        Prompts[prompts/<br/>System Prompts]
    end

    TG <-->|Polling| Bot
    Bot --> Handler
    Handler --> LLM
    Handler --> DM
    LLM -->|HTTP| OR
    DM --> Memory

    Config --> ENV
    Config --> Prompts
    Main --> Config
    Main --> Bot
    Main --> Handler
    Main --> LLM
    Main --> DM

    Handler -.->|structlog| Logs
    LLM -.->|structlog| Logs

    style TG fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style OR fill:#E91E63,stroke:#C2185B,stroke-width:3px,color:#fff
    style Bot fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style Handler fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style LLM fill:#9C27B0,stroke:#7B1FA2,stroke-width:3px,color:#fff
    style DM fill:#00BCD4,stroke:#0097A7,stroke-width:3px,color:#fff
    style Config fill:#607D8B,stroke:#455A64,stroke-width:3px,color:#fff
    style Main fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style Memory fill:#FF5722,stroke:#D84315,stroke-width:2px,color:#fff
    style Logs fill:#795548,stroke:#5D4037,stroke-width:2px,color:#fff
    style ENV fill:#FFC107,stroke:#FFA000,stroke-width:2px,color:#000
    style Prompts fill:#CDDC39,stroke:#AFB42B,stroke-width:2px,color:#000
```

### Компонентная архитектура

```mermaid
graph LR
    subgraph Layer1["Presentation Layer"]
        Bot[Bot]
        Handler[MessageHandler]
    end

    subgraph Layer2["Business Logic Layer"]
        DM[DialogManager]
        LLM[LLMClient]
    end

    subgraph Layer3["Data Layer"]
        Memory[(In-Memory<br/>Storage)]
    end

    subgraph Layer4["Integration Layer"]
        TG_API[Telegram API]
        OR_API[Openrouter API]
    end

    subgraph Config_Layer["Configuration Layer"]
        Config[Config]
        ENV[.env]
        Prompts[prompts/]
    end

    Bot --> Handler
    Handler --> DM
    Handler --> LLM
    DM --> Memory

    Bot <--> TG_API
    LLM <--> OR_API

    Config --> ENV
    Config --> Prompts
    Bot -.->|uses| Config
    Handler -.->|uses| Config
    LLM -.->|uses| Config
    DM -.->|uses| Config

    style Bot fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style Handler fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style DM fill:#00BCD4,stroke:#0097A7,stroke-width:3px,color:#fff
    style LLM fill:#9C27B0,stroke:#7B1FA2,stroke-width:3px,color:#fff
    style Memory fill:#FF5722,stroke:#D84315,stroke-width:3px,color:#fff
    style TG_API fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style OR_API fill:#E91E63,stroke:#C2185B,stroke-width:3px,color:#fff
    style Config fill:#607D8B,stroke:#455A64,stroke-width:3px,color:#fff
```

---

## Поток данных

### Обработка текстового сообщения

```mermaid
sequenceDiagram
    autonumber
    participant U as 👤 User
    participant T as Telegram API
    participant B as Bot
    participant H as Handler
    participant DM as DialogManager
    participant M as Memory
    participant L as LLMClient
    participant O as Openrouter
    participant Log as structlog

    U->>T: Send text message
    T->>B: getUpdates (polling)
    B->>H: dispatch message event

    H->>H: Validate (text, from_user)
    H->>Log: message_received

    H->>DM: add_message(user_id, "user", text)
    DM->>M: Append to history

    H->>DM: get_history(user_id)
    DM->>M: Read history
    DM->>DM: Apply trim (if MAX_CONTEXT > 0)
    DM-->>H: Return history

    H->>L: generate_response(history)
    L->>Log: llm_request
    L->>O: POST /chat/completions
    O-->>L: Response with content
    L->>Log: llm_response
    L-->>H: Return content

    H->>DM: add_message(user_id, "assistant", content)
    DM->>M: Append to history

    H->>B: send message
    B->>T: sendMessage
    T->>U: Receive response

    Note over H,L: Error handling wraps all operations
```

### Обработка команды /clear

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant T as Telegram API
    participant B as Bot
    participant H as Handler
    participant DM as DialogManager
    participant M as Memory

    U->>T: /clear
    T->>B: getUpdates
    B->>H: dispatch command

    H->>H: Validate from_user
    H->>DM: clear_history(user_id)
    DM->>M: Delete dialogs[user_id]
    DM-->>H: Done

    H->>B: send "История диалога очищена"
    B->>T: sendMessage
    T->>U: Receive confirmation
```

### Первое обращение пользователя

```mermaid
sequenceDiagram
    participant U as 👤 New User
    participant H as Handler
    participant DM as DialogManager
    participant C as Config
    participant M as Memory

    U->>H: First message
    H->>DM: get_history(new_user_id)

    alt User history not exists
        DM->>DM: Check dialogs[user_id]
        DM->>C: Get SYSTEM_PROMPT
        C-->>DM: Return system prompt
        DM->>M: Create [{role: "system", content: prompt}]
        DM-->>H: Return new history with system prompt
    end

    Note over H,M: History now initialized<br/>with system prompt
```

---

## Граф зависимостей

### Импорты и зависимости модулей

```mermaid
graph TD
    main[main.py] -->|creates| config[config.py]
    main -->|creates| bot[bot.py]
    main -->|creates| handler[handler.py]
    main -->|creates| llm[llm_client.py]
    main -->|creates| dm[dialog_manager.py]
    main -->|uses| structlog[structlog]

    bot -->|imports| aiogram_bot[aiogram.Bot]
    bot -->|imports| aiogram_dp[aiogram.Dispatcher]
    bot -->|depends on| config

    handler -->|imports| aiogram_router[aiogram.Router]
    handler -->|imports| aiogram_types[aiogram.types]
    handler -->|depends on| llm
    handler -->|depends on| dm
    handler -->|depends on| structlog

    llm -->|imports| openai[openai.AsyncOpenAI]
    llm -->|depends on| config
    llm -->|depends on| structlog

    dm -->|depends on| config

    config -->|imports| dotenv[python-dotenv]
    config -->|reads| env[.env file]
    config -->|reads| prompts[prompts/*.txt]

    style main fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style config fill:#607D8B,stroke:#455A64,stroke-width:3px,color:#fff
    style bot fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style handler fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style llm fill:#9C27B0,stroke:#7B1FA2,stroke-width:3px,color:#fff
    style dm fill:#00BCD4,stroke:#0097A7,stroke-width:3px,color:#fff
    style aiogram_bot fill:#2196F3,stroke:#1976D2,stroke-width:2px,color:#fff
    style aiogram_dp fill:#2196F3,stroke:#1976D2,stroke-width:2px,color:#fff
    style aiogram_router fill:#2196F3,stroke:#1976D2,stroke-width:2px,color:#fff
    style aiogram_types fill:#2196F3,stroke:#1976D2,stroke-width:2px,color:#fff
    style openai fill:#E91E63,stroke:#C2185B,stroke-width:2px,color:#fff
    style structlog fill:#795548,stroke:#5D4037,stroke-width:2px,color:#fff
    style dotenv fill:#8BC34A,stroke:#689F38,stroke-width:2px,color:#fff
    style env fill:#FFC107,stroke:#FFA000,stroke-width:2px,color:#000
    style prompts fill:#CDDC39,stroke:#AFB42B,stroke-width:2px,color:#000
```

### Инъекция зависимостей (DI)

```mermaid
graph TB
    subgraph main.py
        M[main()]
    end

    M -->|1. Create| C[Config]
    M -->|2. Create| L[Logger]
    M -->|3. Create| B[Bot]
    M -->|4. Create with Config+Logger| LLC[LLMClient]
    M -->|5. Create with Config| DM[DialogManager]
    M -->|6. Create with LLC+DM+Logger| H[MessageHandler]
    M -->|7. Register| R[Router]
    M -->|8. Start| P[Polling]

    C -.->|inject| B
    C -.->|inject| LLC
    C -.->|inject| DM
    L -.->|inject| LLC
    L -.->|inject| H
    LLC -.->|inject| H
    DM -.->|inject| H

    style M fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style C fill:#607D8B,stroke:#455A64,stroke-width:3px,color:#fff
    style L fill:#795548,stroke:#5D4037,stroke-width:3px,color:#fff
    style B fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style LLC fill:#9C27B0,stroke:#7B1FA2,stroke-width:3px,color:#fff
    style DM fill:#00BCD4,stroke:#0097A7,stroke-width:3px,color:#fff
    style H fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
```

---

## Последовательность взаимодействий

### Полный цикл: от запуска до ответа

```mermaid
sequenceDiagram
    autonumber
    participant Dev as 👨‍💻 Developer
    participant OS as Operating System
    participant Main as main.py
    participant Config as Config
    participant Bot as Bot
    participant DP as Dispatcher
    participant TG as Telegram API
    participant User as 👤 User

    Dev->>OS: make run
    OS->>Main: python -m src.main

    Main->>Config: Config()
    Config->>Config: load_dotenv()
    Config->>Config: validate required params
    Config-->>Main: config instance

    Main->>Main: setup_logging(config)

    Main->>Bot: Bot(config)
    Bot->>Bot: Create aiogram.Bot
    Bot->>Bot: Create Dispatcher
    Bot-->>Main: bot instance

    Main->>Main: Create LLMClient, DialogManager, Handler
    Main->>DP: dp.include_router(handler.router)

    Main->>Bot: bot.start()
    Bot->>TG: Start polling

    loop Every N seconds
        TG->>Bot: Check for updates

        alt New message
            TG-->>Bot: Update with message
            Bot->>DP: Dispatch
            Note over DP,User: Handle message<br/>(see previous diagrams)
        end
    end
```

### Обработка ошибок в LLM

```mermaid
sequenceDiagram
    participant H as Handler
    participant L as LLMClient
    participant O as Openrouter
    participant Log as structlog
    participant U as 👤 User

    H->>L: generate_response(history)
    L->>Log: llm_request
    L->>O: POST /chat/completions

    alt Success
        O-->>L: 200 OK with content
        L->>Log: llm_response
        L-->>H: content
        H->>U: Send content
    else API Error
        O-->>L: 401/403/429 Error
        L->>Log: llm_api_error (exc_info=True)
        L-->>H: Raise OpenAIError
        H->>Log: llm_error
        H->>U: "Произошла ошибка, попробуйте позже"
    else Timeout
        O-->>L: Timeout
        L->>Log: llm_timeout_error (exc_info=True)
        L-->>H: Raise TimeoutError
        H->>Log: llm_error
        H->>U: "Произошла ошибка, попробуйте позже"
    end
```

---

## Жизненный цикл сообщения

### Состояния обработки

```mermaid
stateDiagram-v2
    [*] --> Received: User sends message

    Received --> Validating: Handler gets event
    Validating --> Invalid: No text or from_user
    Validating --> Valid: Has text and from_user

    Invalid --> [*]: Ignore (early return)

    Valid --> AddingToHistory: add_message(user)
    AddingToHistory --> RetrievingHistory: get_history()
    RetrievingHistory --> Trimming: Check MAX_CONTEXT

    Trimming --> SendingToLLM: History ready
    SendingToLLM --> WaitingResponse: HTTP request

    WaitingResponse --> Success: Got response
    WaitingResponse --> Error: API error

    Success --> SavingResponse: add_message(assistant)
    SavingResponse --> SendingToUser: Prepare answer
    SendingToUser --> [*]: Message sent

    Error --> LoggingError: Log with exc_info
    LoggingError --> SendingError: Send error message
    SendingError --> [*]: Error handled

    note right of Received
        Logged: message_received
    end note

    note right of SendingToLLM
        Logged: llm_request
    end note

    note right of Success
        Logged: llm_response
    end note

    note right of Error
        Logged: llm_error
    end note
```

### Жизненный цикл истории диалога

```mermaid
stateDiagram-v2
    [*] --> NotExists: New user_id

    NotExists --> Initialized: get_history()

    state Initialized {
        [*] --> SystemPrompt: Create with system prompt
        SystemPrompt --> Ready
    }

    Initialized --> Growing: add_message()

    state Growing {
        [*] --> AddUser: user message
        AddUser --> AddAssistant: assistant response
        AddAssistant --> [*]
    }

    Growing --> Growing: More messages
    Growing --> Trimmed: get_history() with MAX_CONTEXT > 0

    state Trimmed {
        [*] --> KeepSystem: Preserve system prompt
        KeepSystem --> KeepLastN: Keep last N*2 messages
        KeepLastN --> [*]
    }

    Trimmed --> Growing: add_message()

    Growing --> Deleted: clear_history()
    Trimmed --> Deleted: clear_history()

    Deleted --> [*]

    note right of NotExists
        dialogs[user_id] not in dict
    end note

    note right of Initialized
        dialogs[user_id] = [system_prompt]
    end note

    note right of Deleted
        del dialogs[user_id]
    end note
```

---

## Структура хранения

### In-Memory Storage структура

```mermaid
graph TB
    subgraph DialogManager
        DM[dialog_manager.py]
        Dialogs[dialogs: dict]
    end

    Dialogs -->|key| U1[user_id: 12345]
    Dialogs -->|key| U2[user_id: 67890]
    Dialogs -->|key| U3[user_id: 11111]

    U1 -->|value| H1[History List]
    U2 -->|value| H2[History List]
    U3 -->|value| H3[History List]

    subgraph H1[History: user 12345]
        M1_1[0: system prompt]
        M1_2[1: user message 1]
        M1_3[2: assistant response 1]
        M1_4[3: user message 2]
        M1_5[4: assistant response 2]
    end

    subgraph H2[History: user 67890]
        M2_1[0: system prompt]
        M2_2[1: user message 1]
    end

    subgraph H3[History: user 11111]
        M3_1[0: system prompt]
        M3_2[1: user message 1]
        M3_3[2: assistant response 1]
        M3_4[3: user message 2]
        M3_5[4: assistant response 2]
        M3_6[5: user message 3]
        M3_7[6: assistant response 3]
    end

    style DM fill:#00BCD4,stroke:#0097A7,stroke-width:3px,color:#fff
    style Dialogs fill:#FF5722,stroke:#D84315,stroke-width:3px,color:#fff
    style U1 fill:#2196F3,stroke:#1976D2,stroke-width:2px,color:#fff
    style U2 fill:#2196F3,stroke:#1976D2,stroke-width:2px,color:#fff
    style U3 fill:#2196F3,stroke:#1976D2,stroke-width:2px,color:#fff
    style M1_1 fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
    style M2_1 fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
    style M3_1 fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
```

### Message формат (OpenAI API)

```mermaid
classDiagram
    class Message {
        +string role
        +string content
    }

    class SystemMessage {
        role = "system"
        content: System prompt text
    }

    class UserMessage {
        role = "user"
        content: User input text
    }

    class AssistantMessage {
        role = "assistant"
        content: LLM response text
    }

    Message <|-- SystemMessage
    Message <|-- UserMessage
    Message <|-- AssistantMessage

    class History {
        +list~Message~ messages
        +add_message(role, content)
        +get_last_n(n)
        +clear()
    }

    History "1" --> "*" Message : contains
```

### Обрезка контекста (Trimming)

```mermaid
flowchart TD
    Start[get_history] --> Check{MAX_CONTEXT > 0?}

    Check -->|No| Return[Return full history]
    Check -->|Yes| Trim[_trim_history]

    Trim --> ExtractSystem[Extract system prompt<br/>history0]
    ExtractSystem --> ExtractDialog[Extract dialog messages<br/>history1 to end]

    ExtractDialog --> CalcMax[max_dialog = MAX_CONTEXT * 2]
    CalcMax --> CheckLen{len(dialog) > max_dialog?}

    CheckLen -->|No| Combine1[system + dialog]
    CheckLen -->|Yes| Slice[dialog = dialog-max_dialog:]

    Slice --> Combine2[system + last N*2 messages]

    Combine1 --> ReturnTrimmed[Return history]
    Combine2 --> ReturnTrimmed
    Return --> End[End]
    ReturnTrimmed --> End

    style Start fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style Trim fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style ReturnTrimmed fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style End fill:#9C27B0,stroke:#7B1FA2,stroke-width:3px,color:#fff
```

---

## Обработка ошибок

### Стратегия обработки ошибок

```mermaid
graph TB
    subgraph Config_Errors["Config Layer Errors"]
        CE1[Missing env var] --> Fail1[ValueError<br/>Fail Fast]
        CE2[File not found] --> Fail1
        CE3[Invalid config] --> Fail1
        Fail1 --> Stop[Bot doesn't start]
    end

    subgraph LLM_Errors["LLM Layer Errors"]
        LE1[OpenAIError] --> Log1[Log with exc_info]
        LE2[TimeoutError] --> Log1
        LE3[RateLimitError] --> Log1
        Log1 --> Raise[Re-raise exception]
    end

    subgraph Handler_Errors["Handler Layer Errors"]
        Raise --> Catch[Exception caught]
        Catch --> Log2[Log llm_error]
        Log2 --> User[Send user-friendly message]
        User --> Continue[Continue processing]
    end

    subgraph Validation_Errors["Validation Errors"]
        VE1[No message.text] --> EarlyReturn[Early return<br/>Silent ignore]
        VE2[No message.from_user] --> EarlyReturn
        EarlyReturn --> Next[Process next message]
    end

    style Fail1 fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style Stop fill:#000000,stroke:#000000,stroke-width:3px,color:#fff
    style Log1 fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style Log2 fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style Raise fill:#E91E63,stroke:#C2185B,stroke-width:3px,color:#fff
    style Catch fill:#9C27B0,stroke:#7B1FA2,stroke-width:3px,color:#fff
    style User fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style Continue fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style EarlyReturn fill:#607D8B,stroke:#455A64,stroke-width:3px,color:#fff
```

### Обработка ошибок по слоям

```mermaid
flowchart LR
    subgraph Layer1["Config Layer"]
        C1[Validation] -->|Error| F1[Fail Fast<br/>ValueError]
        F1 --> Exit1[Exit]
    end

    subgraph Layer2["LLM Layer"]
        L1[API Call] -->|Error| L2[Log + Re-raise]
        L2 --> Pass1[Pass to Handler]
    end

    subgraph Layer3["Handler Layer"]
        Pass1 --> H1[Catch Exception]
        H1 --> H2[Log Error]
        H2 --> H3[User Message]
        H3 --> H4[Continue]
    end

    subgraph Layer4["Bot Layer"]
        H4 --> B1[Next Update]
        B1 --> B2[Keep Running]
    end

    style F1 fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style Exit1 fill:#000000,stroke:#000000,stroke-width:2px,color:#fff
    style L2 fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style H1 fill:#9C27B0,stroke:#7B1FA2,stroke-width:3px,color:#fff
    style H2 fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style H3 fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style B2 fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
```

---

## Структура проекта

### Mindmap структуры

```mermaid
mindmap
  root((telegram-bot))
    src
      main.py
        Entry Point
        DI Container
        Setup Logging
      config.py
        Load .env
        Validate params
        System prompt
      bot.py
        aiogram Bot
        Dispatcher
        Polling
      handler.py
        Commands
        Text messages
        Routing
      llm_client.py
        AsyncOpenAI
        Error handling
        Logging
      dialog_manager.py
        In-memory storage
        History management
        Context trimming
    tests
      conftest.py
        Fixtures
        Mocks
      unit
        test_config.py
        test_dialog_manager.py
        test_llm_client.py
      integration
        test_handler.py
    docs
      guides
        00-11 guides
        README
      tasklists
        tasklist-s0.md
        tasklist_tech_debt-s0.md
      vision.md
      roadmap.md
    prompts
      music_consultant.txt
      Other roles
    Config Files
      .env
        Secrets
        API keys
      .env.example
        Template
      pyproject.toml
        Dependencies
        Tool config
      Makefile
        Commands
```

### Дерево файловой системы

```mermaid
graph TB
    Root[telegram-bot/] --> Src[src/]
    Root --> Tests[tests/]
    Root --> Docs[docs/]
    Root --> Prompts[prompts/]
    Root --> Logs[logs/]
    Root --> Config[Config Files]

    Src --> S1[__init__.py]
    Src --> S2[main.py]
    Src --> S3[config.py]
    Src --> S4[bot.py]
    Src --> S5[handler.py]
    Src --> S6[llm_client.py]
    Src --> S7[dialog_manager.py]

    Tests --> T1[conftest.py]
    Tests --> TU[unit/]
    Tests --> TI[integration/]

    TU --> TU1[test_config.py]
    TU --> TU2[test_dialog_manager.py]
    TU --> TU3[test_llm_client.py]

    TI --> TI1[test_handler.py]

    Docs --> D1[guides/]
    Docs --> D2[vision.md]
    Docs --> D3[roadmap.md]
    Docs --> D4[tasklists/]

    D1 --> G1[00-11 guides]
    D1 --> G2[README.md]

    D4 --> TL1[tasklist-s0.md]
    D4 --> TL2[tasklist_tech_debt-s0.md]

    Prompts --> P1[music_consultant.txt]

    Config --> C1[.env]
    Config --> C2[.env.example]
    Config --> C3[pyproject.toml]
    Config --> C4[Makefile]
    Config --> C5[README.md]

    style Root fill:#F44336,stroke:#C62828,stroke-width:3px,color:#fff
    style Src fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style Tests fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style Docs fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style Prompts fill:#9C27B0,stroke:#7B1FA2,stroke-width:3px,color:#fff
    style Logs fill:#795548,stroke:#5D4037,stroke-width:3px,color:#fff
    style Config fill:#607D8B,stroke:#455A64,stroke-width:3px,color:#fff
```

---

## Timeline разработки

### История итераций

```mermaid
timeline
    title Развитие проекта
    section Phase 1: MVP
        Итерация 1 (2025-10-10) : Инициализация проекта
                                 : Config + .env
                                 : uv + Makefile
        Итерация 2 (2025-10-10) : Базовый бот
                                 : aiogram setup
                                 : /start команда
        Итерация 3 (2025-10-10) : LLM интеграция
                                 : LLMClient
                                 : Openrouter API
    section Phase 2: Core Features
        Итерация 4 (2025-10-11) : История диалогов
                                 : DialogManager
                                 : /clear команда
        Итерация 5 (2025-10-11) : Логирование
                                 : structlog
                                 : Error handling
        Итерация 6 (2025-10-11) : /role команда
                                 : TDD workflow
                                 : BOT_ROLE_* params
        Итерация 7 (2025-10-11) : Промпты из файлов
                                 : prompts/ директория
                                 : SYSTEM_PROMPT_FILE
    section Phase 3: Quality
        Tech Debt 1 (2025-10-11) : Критичные фиксы
                                  : Валидация
                                  : Context trimming
        Tech Debt 2 (2025-10-11) : Инструменты
                                  : ruff + mypy
                                  : Makefile commands
        Tech Debt 3 (2025-10-11) : Тестирование
                                  : pytest setup
                                  : Unit + Integration
```

### Roadmap (текущее состояние)

```mermaid
graph LR
    subgraph Completed["✅ Завершено"]
        C1[MVP<br/>Итерации 1-7]
        C2[Quality Tools<br/>Tech Debt 1-3]
        C3[Documentation<br/>12 Guides]
    end

    subgraph InProgress["🟡 Планируется"]
        P1[Tech Debt 4<br/>Рефакторинг]
    end

    subgraph Future["⚪ Будущее"]
        F1[CI/CD<br/>Automation]
        F2[Persistence<br/>SQLite/PostgreSQL]
        F3[Advanced Features<br/>Voice, RAG, etc]
    end

    C1 --> C2
    C2 --> C3
    C3 --> P1
    P1 -.->|После завершения| F1
    P1 -.->|После завершения| F2
    F1 -.-> F3
    F2 -.-> F3

    style C1 fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style C2 fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style C3 fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style P1 fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style F1 fill:#9E9E9E,stroke:#616161,stroke-width:2px,color:#fff
    style F2 fill:#9E9E9E,stroke:#616161,stroke-width:2px,color:#fff
    style F3 fill:#9E9E9E,stroke:#616161,stroke-width:2px,color:#fff
```

---

## Makefile команды

### Граф команд и зависимостей

```mermaid
graph TB
    subgraph Development["Development Commands"]
        Install[make install<br/>uv sync]
        Run[make run<br/>python -m src.main]
    end

    subgraph Quality["Quality Commands"]
        Format[make format<br/>ruff format]
        Lint[make lint<br/>ruff check + mypy]
        Fix[make fix<br/>ruff --fix]
    end

    subgraph Testing["Testing Commands"]
        Test[make test<br/>pytest]
        TestCov[make test-cov<br/>pytest --cov]
    end

    subgraph Workflow["Pre-commit Workflow"]
        Code[Write Code] --> Format
        Format --> Lint
        Lint --> LintOK{Errors?}
        LintOK -->|Yes| Fix
        Fix --> Lint
        LintOK -->|No| Test
        Test --> TestOK{Pass?}
        TestOK -->|Yes| Commit[git commit]
        TestOK -->|No| Code
    end

    Install -.->|Required for| Run
    Install -.->|Required for| Format
    Install -.->|Required for| Lint
    Install -.->|Required for| Test

    style Install fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
    style Run fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style Format fill:#9C27B0,stroke:#7B1FA2,stroke-width:3px,color:#fff
    style Lint fill:#FF9800,stroke:#F57C00,stroke-width:3px,color:#fff
    style Fix fill:#FF5722,stroke:#D84315,stroke-width:3px,color:#fff
    style Test fill:#00BCD4,stroke:#0097A7,stroke-width:3px,color:#fff
    style TestCov fill:#00BCD4,stroke:#0097A7,stroke-width:3px,color:#fff
    style Commit fill:#4CAF50,stroke:#388E3C,stroke-width:3px,color:#fff
```

### Команды по категориям

```mermaid
mindmap
  root((Makefile<br/>Commands))
    Setup
      make install
        uv sync
        Install dependencies
    Run
      make run
        python -m src.main
        Start bot
    Code Quality
      make format
        ruff format src/
        Auto-format code
      make lint
        ruff check src/
        mypy src/
        Static analysis
      make fix
        ruff --fix
        Auto-fix issues
    Testing
      make test
        pytest tests/ -v
        Run all tests
      make test-cov
        pytest --cov
        Coverage report
    Cleanup
      make clean
        Remove cache
        Remove logs
```

---

## Интеграционные точки

### Внешние API и сервисы

```mermaid
graph TB
    subgraph Bot["🤖 Telegram Bot"]
        Core[Core Application]
    end

    subgraph External["🌐 External Services"]
        TG[Telegram Bot API]
        OR[Openrouter API]
    end

    subgraph Resources["📦 Resources"]
        ENV[.env<br/>Environment]
        Files[prompts/<br/>System Prompts]
    end

    subgraph Monitoring["📊 Monitoring"]
        Logs[logs/<br/>JSON Logs]
        Console[stdout<br/>Console Output]
    end

    Core <-->|Polling<br/>getUpdates| TG
    Core <-->|HTTP POST<br/>/chat/completions| OR
    Core -->|Load| ENV
    Core -->|Read| Files
    Core -->|Write| Logs
    Core -->|Print| Console

    TG -.->|Webhook<br/>не реализовано| Core
    OR -.->|Streaming<br/>не реализовано| Core

    style Core fill:#FF5722,stroke:#D84315,stroke-width:4px,color:#fff
    style TG fill:#2196F3,stroke:#1976D2,stroke-width:3px,color:#fff
    style OR fill:#E91E63,stroke:#C2185B,stroke-width:3px,color:#fff
    style ENV fill:#FFC107,stroke:#FFA000,stroke-width:2px,color:#000
    style Files fill:#CDDC39,stroke:#AFB42B,stroke-width:2px,color:#000
    style Logs fill:#795548,stroke:#5D4037,stroke-width:2px,color:#fff
    style Console fill:#607D8B,stroke:#455A64,stroke-width:2px,color:#fff
```

### Протокол взаимодействия с Telegram

```mermaid
sequenceDiagram
    participant B as Bot (Polling)
    participant T as Telegram API

    loop Every N seconds
        B->>T: GET /getUpdates<br/>offset=last_update_id

        alt Has new updates
            T-->>B: 200 OK<br/>[{update_id, message}]
            B->>B: Process each update
            B->>B: Update offset = last_update_id + 1
        else No updates
            T-->>B: 200 OK<br/>[]
        else Error
            T-->>B: 4xx/5xx Error
            B->>B: Log error, retry
        end
    end
```

### Протокол взаимодействия с Openrouter

```mermaid
sequenceDiagram
    participant L as LLMClient
    participant O as Openrouter API

    L->>O: POST /chat/completions<br/>Authorization: Bearer key<br/>Body: {model, messages}

    alt Success
        O-->>L: 200 OK<br/>{choices: [{message: {content}}]}
        L->>L: Extract content
    else Invalid Key
        O-->>L: 401 Unauthorized
        L->>L: Raise OpenAIError
    else Rate Limit
        O-->>L: 429 Too Many Requests
        L->>L: Raise OpenAIError
    else Insufficient Credits
        O-->>L: 402 Payment Required
        L->>L: Raise OpenAIError
    else Server Error
        O-->>L: 500 Internal Server Error
        L->>L: Raise OpenAIError
    else Network Timeout
        O-->>L: Timeout
        L->>L: Raise TimeoutError
    end
```

---

## Навигация по гайдам

### Связь визуализации с документацией

```mermaid
graph TD
    Visual[12_visual_project_overview.md<br/>Эта страница]

    Visual -.->|Архитектура детально| G01[01_architecture_overview.md]
    Visual -.->|Навигация по коду| G02[02_codebase_tour.md]
    Visual -.->|Форматы данных| G03[03_data_model.md]
    Visual -.->|API интеграции| G04[04_integrations.md]
    Visual -.->|Конфигурация| G05[05_configuration_secrets.md]
    Visual -.->|Workflow разработки| G06[06_development_workflow.md]
    Visual -.->|Тестирование| G07[07_testing_guide.md]
    Visual -.->|Обработка ошибок| G10[10_troubleshooting.md]
    Visual -.->|Расширение проекта| G11[11_extending_project.md]

    style Visual fill:#F44336,stroke:#C62828,stroke-width:4px,color:#fff
    style G01 fill:#2196F3,stroke:#1976D2,stroke-width:2px,color:#fff
    style G02 fill:#4CAF50,stroke:#388E3C,stroke-width:2px,color:#fff
    style G03 fill:#FF9800,stroke:#F57C00,stroke-width:2px,color:#fff
    style G04 fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#fff
    style G05 fill:#00BCD4,stroke:#0097A7,stroke-width:2px,color:#fff
    style G06 fill:#E91E63,stroke:#C2185B,stroke-width:2px,color:#fff
    style G07 fill:#FFC107,stroke:#FFA000,stroke-width:2px,color:#000
    style G10 fill:#795548,stroke:#5D4037,stroke-width:2px,color:#fff
    style G11 fill:#607D8B,stroke:#455A64,stroke-width:2px,color:#fff
```

---

## Заключение

Этот гайд предоставляет визуальное представление проекта с различных точек зрения:

✅ **Архитектурная** - компоненты и их связи
✅ **Динамическая** - потоки данных и последовательности
✅ **Структурная** - организация кода и зависимости
✅ **Состояния** - жизненные циклы объектов
✅ **Хранение** - модели данных и форматы
✅ **Обработка ошибок** - стратегии и слои
✅ **Процессы** - workflows и команды
✅ **История** - timeline развития

Для детального изучения каждого аспекта обращайтесь к соответствующим гайдам из [docs/guides/](README.md).

---

**Последнее обновление**: 2025-10-16
**Версия**: 1.0
