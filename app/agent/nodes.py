import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage

from app.agent.state import AgentState
from app.agent.tools import (
    get_customer,
    get_order,
    get_refund_policy,
    search_knowledge,
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=api_key,
)

llm_with_tools = llm.bind_tools(
    [
        get_order,
        get_customer,
        get_refund_policy,
        search_knowledge
    ]
)


def call_llm(state: AgentState):
    messages = state["messages"]

    if state["summary"]:
        messages = [
            SystemMessage(
                content=f"""
Here is a summary of the earlier conversation:

{state["summary"]}

Use this summary as additional context when answering the user.
"""
            )
        ] + messages

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }