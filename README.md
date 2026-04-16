# CrewAI Projects Repository

A collection of CrewAI projects demonstrating various agentic AI patterns including code execution, debates, financial research, and multi-crew orchestration.

## Repository Structure

```
crewai/
├── coder/               # AI coding assistant with code execution
├── debate/              # Multi-agent debate system
├── financial_researcher/ # Research crew with web search
└── latest_ai_flow/     # Flow-based multi-crew orchestration
```

---

## Project 1: Coder (`coder/`)

**Purpose**: AI coding assistant that writes and executes Python code with safety constraints.

### Architecture

| Component | Type | Description |
|-----------|------|-------------|
| `Coder` | Agent | Single agent with code execution capabilities |

### Key Features

- **Code Execution**: Enabled with `allow_code_execution=True`
- **Safety Mode**: Uses Docker for sandboxed execution (`code_execution_mode="safe"`)
- **LLM**: OpenRouter (GPT-4.1-nano) with 15K max tokens
- **Timeout**: 30 second execution limit with 3 retry attempts

### Configuration

- **Process**: Sequential
- **Input**: Mathematical series assignment
- **Output**: Python code with calculated results

### Files

```
coder/
├── src/coder/
│   ├── crew.py          # Crew definition with code execution agent
│   └── main.py          # Entry point with series calculation task
├── config/              # Agent and task YAML configs
├── knowledge/           # Domain knowledge files
└── output/              # Generated outputs
```

### Running

```bash
cd coder
crewai run
# Or directly:
python src/coder/main.py
```

---

## Project 2: Debate (`debate/`)

**Purpose**: Multi-agent debate system with proposer, opposer, and judge roles.

### Architecture

| Component | Type | Description |
|-----------|------|-------------|
| `debater` | Agent | Argues the motion position |
| `judge` | Agent | Evaluates debate arguments |

### Task Flow

```
propose (debater) → oppose (debater) → decide (judge)
```

### Key Features

- **LLM**: OpenRouter (GPT-4.1-nano) with 15K max tokens
- **Process**: Sequential (propose → oppose → judge)
- **Customizable Motion**: Debatable topics passed as input

### Files

```
debate/
├── src/debate/
│   ├── crew.py          # Crew with debater & judge agents
│   ├── main.py          # Entry point with motion input
│   └── tools/           # Custom debate tools
├── config/              # Agent and task YAML configs
└── knowledge/           # Debate knowledge base
```

### Running

```bash
cd debate
crewai run
```

---

## Project 3: Financial Researcher (`financial_researcher/`)

**Purpose**: Research crew that analyzes companies using web search and generates reports.

### Architecture

| Component | Type | Tools | Description |
|-----------|------|-------|-------------|
| `researcher` | Agent | SerperDevTool | Web search for company info |
| `analyst` | Agent | - | Analyzes and synthesizes findings |

### Task Flow

```
research_task (researcher) → analysis_task (analyst) → report.md
```

### Key Features

- **LLM**: OpenRouter (GPT-4.1-nano)
- **Tools**: SerperDevTool for web search
- **Process**: Sequential
- **Output**: Markdown report saved to `output/report.md`

### Files

```
financial_researcher/
├── src/financial_researcher/
│   ├── crew.py          # Research & analysis crew
│   ├── main.py          # Entry point with company input
│   └── tools/           # Custom research tools
├── config/              # Agent and task YAML configs
└── output/              # Generated reports
```

### Running

```bash
cd financial_researcher
crewai run
```

---

## Project 4: Latest AI Flow (`latest_ai_flow/`)

**Purpose**: Advanced flow-based orchestration with multiple crews and state management.

### Architecture

| Component | Type | Description |
|-----------|------|-------------|
| `ResearchFlow` | Flow | State-based workflow orchestrator |
| `ResearchCrew` | Crew | Single-agent research crew |
| `PoemCrew` | Crew | (Available) poem generation crew |

### Flow Structure

```
start (prepare_topic) → listen (run_research) → listen (summarize)
                         ↓
                    ResearchCrew
                    (researcher)
```

### Key Features

- **Flow Orchestration**: Event-driven with `@start` and `@listen` decorators
- **State Management**: Pydantic model (`ResearchFlowState`) for type-safe state
- **Multiple Crews**: Can integrate multiple crews in one flow
- **Tools**: SerperDevTool + WikipediaTools for research
- **Memory**: Enabled on researcher agent

### Files

```
latest_ai_flow/
├── src/latest_ai_flow/
│   ├── main.py              # Flow orchestration entry point
│   ├── crews/
│   │   ├── content_crew/    # Research crew
│   │   └── poem_crew/       # Poem generation crew
│   └── tools/               # Custom flow tools
├── tests/                   # Unit tests
└── output/                  # Generated content
```

### Running

```bash
cd latest_ai_flow
crewai run
# Or for visualization:
crewai flow plot
```

---

## Common Patterns

### LLM Configuration

All projects use OpenRouter for LLM access:

```python
LLM(
    model="openai/gpt-4.1-nano",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    max_tokens=15000,
)
```

### Crew Definition Pattern

```python
@CrewBase
class MyCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def my_agent(self) -> Agent:
        return Agent(config=self.agents_config['my_agent'], ...)

    @task
    def my_task(self) -> Task:
        return Task(config=self.tasks_config['my_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential)
```

### Flow Pattern

```python
class MyFlow(Flow[MyState]):
    @start()
    def begin(self):
        self.state.topic = "AI Agents"

    @listen(begin)
    def research(self):
        result = MyCrew().crew().kickoff(inputs={"topic": self.state.topic})
        self.state.report = result.raw
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| crewai | >=0.108.0 | Core framework |
| crewai-tools | (included) | Built-in tools |
| python-dotenv | (implied) | Environment variables |

---

## Environment Setup

Create `.env` files with:

```env
OPENROUTER_API_KEY=your_key_here
SERPER_API_KEY=your_key_here  # For web search
```

---

## Running All Projects

```bash
# Coder
cd coder && crewai run && cd ..

# Debate
cd debate && crewai run && cd ..

# Financial Researcher
cd financial_researcher && crewai run && cd ..

# Latest AI Flow
cd latest_ai_flow && crewai run && cd ..
```

---

## Project Comparison

| Project | Agents | Tools | Process | Output | Complexity |
|---------|--------|-------|---------|--------|------------|
| coder | 1 | Code Execution | Sequential | Code | Simple |
| debate | 2 | None | Sequential | Verdict | Medium |
| financial_researcher | 2 | SerperDevTool | Sequential | Markdown | Medium |
| latest_ai_flow | 1+ | SerperDevTool, Wikipedia | Flow-based | Variable | Complex |
