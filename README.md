# Multi-Agent Research System

A multi-agent system that uses specialized AI agents to research topics, synthesize findings, and produce structured reports. Built with LangGraph using a supervisor/orchestrator pattern.

## What it does

The system takes a research topic, breaks it into subtopics, gathers information using web search, summarizes the findings, and generates a comprehensive report. Four specialized agents collaborate through a state graph:

```
User Query
    │
    ▼
┌──────────────┐
│ Orchestrator │ ── Creates research plan
└──────────────┘
    │
    ▼
┌──────────────┐
│  Researcher  │ ── Gathers information (web search)
└──────────────┘
    │ (loops for each subtopic)
    ▼
┌──────────────┐
│  Summarizer  │ ── Condenses findings
└──────────────┘
    │
    ▼
┌──────────────┐
│    Writer    │ ── Produces final report
└──────────────┘
    │
    ▼
Final Report
```

- **Orchestrator**: Analyzes the topic and creates a research plan with specific subtopics
- **Researcher**: Uses web search to gather information on each subtopic
- **Summarizer**: Condenses raw research into key insights
- **Writer**: Compiles everything into a structured report

## Setup

```bash
git clone https://github.com/SanaAraj/multi-agent-research.git
cd multi-agent-research
pip install -r requirements.txt
```

Create a `.env` file with your API credentials:

```
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
```

Works with any OpenAI-compatible API provider (OpenAI, Groq, Together, etc.). Just update the base URL accordingly.

## Usage

Run a research query:

```bash
python main.py --topic "Recent advances in quantum computing"
```

Save output to a file:

```bash
python main.py --topic "Climate change mitigation strategies" --output report.md
```

Test with mock responses (no API calls):

```bash
python main.py --topic "Test topic" --mock
```

## Tech Stack

- LangGraph for agent orchestration and state management
- LangChain with OpenAI-compatible LLM client
- DuckDuckGo for web search
- Python 3.10+
