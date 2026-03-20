from typing import TypedDict, Annotated
from operator import add


class ResearchState(TypedDict, total=False):
    topic: str
    research_plan: list[str]
    raw_research: Annotated[list[str], add]
    summaries: Annotated[list[str], add]
    final_report: str
    current_step: str
    current_subtopic_index: int
