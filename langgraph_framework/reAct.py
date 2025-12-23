from typing import Sequence, Annotated, TypedDict
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv


load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],  add_messages]


@tool
def addition(a: int, b: int):
    """add two numbers together"""
    return a + b

@tool
def multiplication(a: int, b: int):
    """multiply two numbers together"""
    return a * b

@tool
def subtraction(a: int, b: int):
    """subtract a number from the other"""
    return a - b

tools = [addition, multiplication, subtraction]

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash').bind_tools(tools)


def our_agent(state: AgentState)-> AgentState:
    system_msg = [SystemMessage(content= 'You are my AI assistant, answer my request to the best of your capability')]

    response = llm.invoke(system_msg + state['messages'])
    return {'messages': response}


def decider(state: AgentState)->AgentState:
    messages = state['messages']

    last_message = messages[-1]

    if not last_message.tool_calls:
        return 'end'
    else:
        return 'continue'


graph = StateGraph(AgentState)

graph.add_node('our_agent', our_agent)
tool_node = ToolNode(tools)
graph.add_node('tools', tool_node)
graph.set_entry_point('our_agent')

graph.add_conditional_edges('our_agent', decider, {
    'end': END,
    'continue': 'tools'
})
graph.add_edge('tools', 'our_agent')

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s['messages'][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {'messages':[HumanMessage(content= 'Add 2 + 5. Then multiply the result by 10. Then also tell me a joke')]}
print_stream(app.stream(inputs, stream_mode='values'))

