from graph.state import AgentState
from tools.web_search import search_web
from db.res import vector_store
def knowledge_agent(state: AgentState):

    print("====== Knowledge Agent ======")


    question = state["question"]

    # Web Search
    web_results = search_web(question)

    # Optional RAG
    rag_results = ""

    if vector_store is not None:

        docs = vector_store.similarity_search(
            question,
            k=3
        )

        rag_results = "\n\n".join(
            doc.page_content
            for doc in docs
        )

    return {

        "web_results": str(web_results),

        "rag_results": rag_results

    }