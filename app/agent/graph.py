from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from app.agent.state import AgentState
from app.agent.nodes import call_llm
from app.agent.tools import (
    get_customer,
    get_order,
    get_refund_policy,
)


def should_use_tools(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


graph_builder = StateGraph(AgentState)

graph_builder.add_node("llm", call_llm)

tool_node = ToolNode(
    [
        get_order,
        get_customer,
        get_refund_policy,
    ]
)

graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "llm")

graph_builder.add_conditional_edges(
    "llm",
    should_use_tools,
)

graph_builder.add_edge("tools", "llm")

graph = graph_builder.compile()