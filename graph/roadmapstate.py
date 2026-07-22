from typing import TypedDict

class RoadmapState(TypedDict):

    goal: str
    level: str
    duration: str
    student_class:int
    hours_per_day: int

    roadmap: str