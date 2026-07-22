from graph.roadmapstate import RoadmapState

def roadmap_planner(state: RoadmapState):

    print("===== Roadmap Planner =====")

    level = state["level"].lower()

    if level == "beginner":
        hours = 2

    elif level == "intermediate":
        hours = 3

    else:
        hours = 4

    return {

        "hours_per_day": hours

    }