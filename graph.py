from langgraph.graph import StateGraph, END
from state import ResearchState
from agents import orchestrator, researcher, summarizer, writer


def should_continue_research(state: ResearchState) -> str:
    idx = state.get("current_subtopic_index", 0)
    plan = state.get("research_plan", [])

    if idx < len(plan):
        return "research"
    return "summarize"


def route_after_orchestrator(state: ResearchState) -> str:
    return "research"


def build_graph(search_func=None):
    graph = StateGraph(ResearchState)

    graph.add_node("orchestrate", orchestrator)
    graph.add_node("research", lambda s: researcher(s, search_func))
    graph.add_node("summarize", summarizer)
    graph.add_node("write", writer)

    graph.set_entry_point("orchestrate")

    graph.add_conditional_edges(
        "orchestrate",
        route_after_orchestrator,
        {"research": "research"},
    )

    graph.add_conditional_edges(
        "research",
        should_continue_research,
        {"research": "research", "summarize": "summarize"},
    )

    graph.add_edge("summarize", "write")
    graph.add_edge("write", END)

    return graph.compile()


def run_research(topic: str, search_func=None) -> str:
    workflow = build_graph(search_func)

    initial_state: ResearchState = {
        "topic": topic,
        "research_plan": [],
        "raw_research": [],
        "summaries": [],
        "final_report": "",
        "current_step": "planning",
        "current_subtopic_index": 0,
    }

    final_state = workflow.invoke(initial_state)
    return final_state.get("final_report", "No report generated.")
