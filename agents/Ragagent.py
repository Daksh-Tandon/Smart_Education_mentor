from graph.quizstate import QuizState
from db.res import vector_store
def rag_agent(state: QuizState):

    print("===== Retrieval Agent =====")



    if vector_store is None:
        return {
            "retrieved_context": "No knowledge base available."
        }

    topic = state["topic"]

    docs = vector_store.similarity_search(
        topic,
        k=4
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return {

        "retrieved_context": context

    }