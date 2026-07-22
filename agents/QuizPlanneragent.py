from graph.quizstate import QuizState

def quiz_planner(state: QuizState):

    print("===== Quiz Planner Agent =====")

    question = state["question"]
    student_class = state["student_class"]

    # ----------------------------
    # Difficulty Logic
    # ----------------------------

    if student_class <= 5:
        difficulty = "Easy"
        question_count = 5

    elif student_class <= 8:
        difficulty = "Medium"
        question_count = 7

    else:
        difficulty = "Hard"
        question_count = 10

    # ----------------------------
    # Subject Detection
    # ----------------------------

    subject = "General"

    science_topics = [
        "photosynthesis",
        "cell",
        "force",
        "electricity",
        "motion",
        "atoms"
    ]

    maths_topics = [
        "algebra",
        "trigonometry",
        "integration",
        "probability"
    ]

    q = question.lower()

    if any(word in q for word in science_topics):
        subject = "Science"

    elif any(word in q for word in maths_topics):
        subject = "Mathematics"

    # ----------------------------
    # Quiz Type
    # ----------------------------

    quiz_type = "MCQ"

    return {

        "topic": question,

        "subject": subject,

        "difficulty": difficulty,

        "question_count": question_count,

        "quiz_type": quiz_type

    }