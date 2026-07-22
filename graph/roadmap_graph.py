from langgraph.graph import StateGraph, END

from graph.roadmapstate import RoadmapState

from agents.roadmapplanner import roadmap_planner
from agents.roadmapgenerator import roadmap_generator


builder = StateGraph(RoadmapState)

builder.add_node(
    "planner",
    roadmap_planner
)

builder.add_node(
    "generator",
    roadmap_generator
)

builder.set_entry_point("planner")

builder.add_edge(
    "planner",
    "generator"
)

builder.add_edge(
    "generator",
    END
)

roadmap_graph = builder.compile()