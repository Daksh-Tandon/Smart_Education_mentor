from graph.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=os.getenv("GOOGLE_API_KEY"),
#     temperature=0
# )

llm = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_KEY"),
    temperature=0
)

def verification_agent(state: AgentState):

    print("====== Verification Agent ======")

    web_results = state["web_results"]
    rag_results = state.get("rag_results", "")
    history = state["messages"][-8:]

    prompt = f"""
    User Conversation History:
{history}

You have two knowledge sources:

1. Web Search Results
2. RAG Results (Educational Notes)

Your task is NOT to explain the topic.
Your task is to produce a verified educational context.

Responsibilities:

1. Remove duplicate information from both sources.
2. Detect conflicting information.
3. Use the conversation history only to resolve references in the current question
   (e.g., "it", "this", "that", "its", "they").
4. If the current question is unrelated to the conversation history, ignore the history completely.
5. Never add facts from the conversation history unless they are supported by the Web Search Results or RAG Results.
6. If Web Search Results and RAG Results conflict, prioritize the RAG Results.
7. If the RAG Results are empty, use the Web Search Results.
8. Merge all verified information into a single educational context.

Output only the verified educational context.
Do not answer the user's question.
Do not invent or assume missing information.

Web Results:
{web_results}

RAG Results:
{rag_results}
"""

    verified_context = llm.invoke(prompt).content
   

    return {
        "verified_context": verified_context
    }