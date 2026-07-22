from typing import TypedDict,Any

class QuizState(TypedDict):

    question: str

    topic: str

    student_class: int

    difficulty: str

    question_count: int

    quiz_type: str

    retrieved_context: str
   

    quiz: list