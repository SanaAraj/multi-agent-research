from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from state import ResearchState
from config import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

_llm = None
_use_mock = True


def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
            model=MODEL_NAME,
            temperature=0.7,
        )
    return _llm


def set_mock_mode(enabled: bool):
    global _use_mock
    _use_mock = enabled


def _call_llm(system_prompt: str, user_prompt: str) -> str:
    if _use_mock:
        return f"[MOCK RESPONSE for: {user_prompt[:50]}...]"

    llm = get_llm()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    response = llm.invoke(messages)
    return response.content


def orchestrator(state: ResearchState) -> dict:
    topic = state["topic"]

    system_prompt = """You are a research planning expert. Given a topic, create a research plan
with 2-3 specific subtopics to investigate. Return ONLY a comma-separated list of subtopics, nothing else."""

    response = _call_llm(system_prompt, f"Create a research plan for: {topic}")

    if _use_mock:
        subtopics = [f"{topic} - History", f"{topic} - Current State", f"{topic} - Future"]
    else:
        subtopics = [s.strip() for s in response.split(",") if s.strip()]

    return {
        "research_plan": subtopics,
        "current_step": "researching",
        "current_subtopic_index": 0,
    }


def researcher(state: ResearchState, search_func=None) -> dict:
    plan = state["research_plan"]
    idx = state.get("current_subtopic_index", 0)

    if idx >= len(plan):
        return {"current_step": "summarizing"}

    subtopic = plan[idx]

    if search_func:
        search_results = search_func(subtopic)
    else:
        search_results = f"[Mock search results for {subtopic}]"

    system_prompt = """You are a research analyst. Given search results about a topic,
extract the key facts and information. Be concise and factual."""

    user_prompt = f"Topic: {subtopic}\n\nSearch Results:\n{search_results}\n\nExtract key information:"

    response = _call_llm(system_prompt, user_prompt)

    if _use_mock:
        response = f"Key findings about {subtopic}: Important fact 1, Important fact 2, Important fact 3."

    return {
        "raw_research": [response],
        "current_subtopic_index": idx + 1,
    }


def summarizer(state: ResearchState) -> dict:
    raw_research = state.get("raw_research", [])

    if not raw_research:
        return {"summaries": ["No research data to summarize."], "current_step": "writing"}

    system_prompt = """You are an expert summarizer. Condense the following research findings
into a clear, concise summary highlighting the most important points."""

    combined = "\n\n".join(raw_research)
    response = _call_llm(system_prompt, f"Summarize:\n{combined}")

    if _use_mock:
        response = f"Summary: The research covered {len(raw_research)} areas with key insights on each topic."

    return {
        "summaries": [response],
        "current_step": "writing",
    }


def writer(state: ResearchState) -> dict:
    topic = state["topic"]
    summaries = state.get("summaries", [])

    system_prompt = """You are a professional report writer. Create a well-structured research report
with an introduction, key findings, and conclusion. Be clear and professional."""

    user_prompt = f"""Write a research report on: {topic}

Research summaries:
{chr(10).join(summaries)}

Create a structured report with Introduction, Key Findings, and Conclusion sections."""

    response = _call_llm(system_prompt, user_prompt)

    if _use_mock:
        response = f"""# Research Report: {topic}

## Introduction
This report examines {topic} based on comprehensive research.

## Key Findings
{chr(10).join(f'- {s}' for s in summaries)}

## Conclusion
The research provides valuable insights into {topic}."""

    return {
        "final_report": response,
        "current_step": "complete",
    }
