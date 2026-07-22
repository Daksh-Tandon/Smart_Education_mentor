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

    prompt = f"""
You are an Educational Verification Agent.

You have two knowledge sources:

1. Web Search Results
2. RAG Results (Educational Notes)

Your job is NOT to explain.

Your responsibilities:

1. Remove duplicate information.
2. Detect conflicting information.
3. If RAG exists and conflicts with Web,
   trust RAG.
4. If RAG is empty,
   use Web results.
5. Merge useful information into one
   verified educational context.

Return ONLY the verified context and the confidence percentage.
Do not add your own knowledge.

Web Results:
{web_results}

RAG Results:
{rag_results}
"""

    verified_context = llm.invoke(prompt).content
   

    return {
        "verified_context": verified_context
    }