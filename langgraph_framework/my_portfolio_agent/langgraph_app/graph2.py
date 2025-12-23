# from langgraph_app.tools.get_free_date import get_free_date
# from langgraph_app.tools.sheet_tool import get_last_row_data
# from langgraph_app.tools.trigger_email import trigger_emails



from typing import TypedDict
from langgraph.graph import StateGraph, END, START

class AgentState(TypedDict):
    userName: str
    userEmail: str
    calendarDate:str



def get_sheet_data(state:AgentState)-> AgentState:
    print('information retrieved successfully')
    # get row information from sheet
    # set agentState with user information
    return state


def get_calendar_info(state: AgentState)-> AgentState:
    print('calendar info retrieved')
    # get calendar information
    return state

def send_emails(state: AgentState)-> AgentState:
    print('email messages dispatched')
    return state


graph = StateGraph(AgentState)

graph.add_node('get_sheet_data', get_sheet_data)
graph.add_node("get_calendar_info", get_calendar_info)
graph.add_node("send_email", send_emails)

graph.add_edge("get_sheet_data", "get_calendar_info")
graph.add_edge("get_calendar_info", "send_email")
# graph.set_finish_point("send_email", END)
graph.set_entry_point("get_sheet_data")

app = graph.compile()
