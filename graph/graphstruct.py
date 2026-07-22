
from agents.evaluationagent import EvaluationAgent


from agents.teachingagent import teaching_agent
from langgraph.graph import StateGraph
from graph.state import AgentState
from agents.verfication_agents import verification_agent
from agents.Knowledgeagent import knowledge_agent
from langgraph.checkpoint.sqlite import SqliteSaver
evaluation_agent = EvaluationAgent()
def evaluation_node(state):

    return evaluation_agent.evaluate(state)


graph = StateGraph(AgentState)
sqlite_cm = SqliteSaver.from_conn_string("memory.db")
checkpointer = sqlite_cm.__enter__()
graph.add_node("knowledge", knowledge_agent)
graph.add_node("verification", verification_agent)


graph.set_entry_point(
    "knowledge"
)





graph.add_edge(
    "knowledge",
    "verification"
)
graph.add_node(
    "teaching",
    teaching_agent
)

graph.add_edge(
    "verification",
    "teaching"

)
graph.add_node(
    "evaluation",
    evaluation_node
)
graph.add_edge(
    "teaching",
    "evaluation"

)



graph_app = graph.compile(checkpointer=checkpointer)
