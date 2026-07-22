from langgraph.graph import StateGraph, END

from graph.quizstate import QuizState

from agents.QuizPlanneragent import quiz_planner
from agents.Ragagent import rag_agent
from agents.Quizgenerator import quiz_generator


builder = StateGraph(QuizState)

# -------------------------
# Nodes
# -------------------------

builder.add_node(
    "planner",
    quiz_planner
)

builder.add_node(
    "retriever",
    rag_agent
)

builder.add_node(
    "generator",
    quiz_generator
)

# -------------------------
# Entry Point
# -------------------------

builder.set_entry_point("planner")

# -------------------------
# Flow
# -------------------------

builder.add_edge(
    "planner",
    "retriever"
)

builder.add_edge(
    "retriever",
    "generator"
)

builder.add_edge(
    "generator",
    END
)

# -------------------------
# Compile
# -------------------------

quiz_graph = builder.compile()