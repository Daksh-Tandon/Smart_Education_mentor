
from graph.quizstate import QuizState
import json
import re

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
llm = ChatOpenAI(
    model="google/gemma-3-12b-it",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_KEY")
)
print(os.getenv("OPEN_ROUTER_KEY"))
def quiz_generator(state: QuizState):

    print("===== Quiz Generator Agent =====")

    context = state["retrieved_context"]

    prompt = f"""
You are an expert school teacher.

Generate exactly {state["question_count"]} MCQs.

Rules:
- Student Class: {state["student_class"]}
- Topic: {state["topic"]}
- Difficulty: {state["difficulty"]}
- if the context {state["retrieved_context"]} does not match with the topic then simply
 say pls upload the pdf in pdf explainer. and return everything empty
- if 
- Each question should have exactly 4 options.
- Only one option should be correct.
- Return ONLY valid json
- Do not use markdown.
- Do not explain anything.

Output Format:

[
    {{
        "question":"...",
        "options":[
            "...",
            "...",
            "...",
            "..."
        ],
        "answer":"..."
    }}
]

Context:

{context}
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    # Remove markdown if present
    content = re.sub(r"```json|```", "", content).strip()

    try:
        quiz = json.loads(content)
    except Exception:
        quiz = {
            "error": "Invalid JSON",
            "raw_output": content
        }

    return {
        "quiz": quiz
    }