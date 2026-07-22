from graph.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
# from datasets import Dataset
# from ragas import evaluate
# from ragas.metrics import Faithfulness, ContextPrecision
load_dotenv()
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("GOOGLE_API_KEY"),
#     temperature=0.4
# )
llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_KEY"),
    temperature=0
)

def teaching_agent(state: AgentState):

    print("====== Teaching Agent ======")

    student_class = state["student_class"]
    verified_context = state["verified_context"]
    question = state["question"]

    prompt = f"""
You are a teacher that uses adaptive way in conversation with students.

Your task is to explain the topic according to the student's class.


Student Class:
{student_class}

Question:
{question}

Verified Context:
{verified_context}

Instructions:

- Explain ONLY using the verified context.
- Use simple language suitable for Class {student_class}.
- Do not introduce facts outside the verified context.
- Give one real-life example.
- Highlight important keywords.
- If the topic contains a formula, explain it.
- End with 3 key takeaways.

Return only the explanation.
"""

    explanation = llm.invoke(prompt).content
    # evaluate_rag(state['question'],state['verified_context'],explanation)
    

    return {
        "explanation": explanation
    }


# def evaluate_rag(question, contexts, answer):

#     dataset = Dataset.from_dict({
#         "user_input": [question],
#         "retrieved_contexts": [contexts],
#         "response": [answer]
#     })

#     result = evaluate(
#         dataset,
#         metrics=[
#             Faithfulness(),
#             ContextPrecision()
#         ]
#     )

#     return result