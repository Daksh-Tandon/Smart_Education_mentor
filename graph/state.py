from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    question: str
    student_class: int

    web_results: str
    rag_results: str
    evaluation:dict

    verified_context: str
    explanation: str
    assessment: str