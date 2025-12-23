from typing import List, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class AgentState(TypedDict):
    messages: List[HumanMessage]


def process (state:AgentState)-> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI resp: {response.content}")
    return {"messages": state["messages"] + [response]}


graph = StateGraph(AgentState)

graph.add_node('processor', process)
graph.add_edge(START, 'processor')
graph.add_edge('processor', END)

app = graph.compile()

user_input = input('Enter: ')

while user_input != 'exit':
    app.invoke({'messages': [HumanMessage(content=user_input)]})
    user_input = input('Enter: ')
