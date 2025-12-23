import os
from dotenv import load_dotenv
from langgraph_sdk import get_sync_client
from langgraph.graph import StateGraph, END

load_dotenv()

LANGGRAPH_API_KEY = os.getenv("LANGGRAPH_API_KEY")
GRAPH_ID = os.getenv("GRAPH_ID", "PortfolioContactAgent")

client = get_sync_client(api_key=LANGGRAPH_API_KEY)

def trigger_portfolio_agent():
    payload = {
        "trigger": "check_sheet_and_send_emails",
        "meta": {
            "spreadsheet_id": os.getenv("SPREADSHEET_ID"),
            "sheet_range": "Sheet1!A:C",
            "admin_email": os.getenv("ADMIN_EMAIL"),
            "calendar_id": os.getenv("CALENDAR_ID")
        }
    }

    thread = client.threads.create()

    response = client.runs.create(
        thread_id=thread["thread_id"],
        assistant_id=GRAPH_ID,
        input=payload
    )
    return response

# ---------------------------
# Helper functions
# ---------------------------

def fetch_last_row_from_sheet(state):
    """Fetches the last row from the Google Sheet."""
    # You can later replace this with real Sheets API logic
    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    sheet_range = "Sheet1!A:D"
    
    print(f"Fetching data from sheet: {spreadsheet_id}")
    # Placeholder: pretend we got the following
    last_row = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "message": "Interested in a consultation"
    }

    return {"last_row": last_row}


def get_next_free_day(state):
    """Fetches the next available free day from Google Calendar."""
    # Placeholder: you’ll connect to Google Calendar API here later
    free_day = "Wednesday, Nov 5th, 2025"
    return {"free_day": free_day}


def send_emails(state):
    """Sends email to user and admin."""
    last_row = state.get("last_row", {})
    free_day = state.get("free_day", "")

    user_email = last_row.get("email")
    user_name = last_row.get("name")
    admin_email = os.getenv("ADMIN_EMAIL")

    print(f"Sending email to user {user_email}...")
    print(f"Sending admin notification to {admin_email}...")

    # Example message body (in production, send via SMTP or SendGrid)
    user_message = (
        f"Hi {user_name},\n\n"
        f"Thanks for reaching out! My next available day for a meeting is {free_day}.\n"
        "Let’s confirm if that works for you.\n\n"
        "Best,\nTemitayo"
    )

    admin_message = (
        f"New inquiry from {user_name} ({user_email}):\n"
        f"Message: {last_row.get('message')}\n"
        f"Suggested free day: {free_day}"
    )

    # Here you can call your mailer function
    print("User message:", user_message)
    print("Admin message:", admin_message)

    return {"status": "emails_sent"}


# ---------------------------
# Build graph flow
# ---------------------------
# Define a state schema (even if simple)
class GraphState(dict):
    """Define what data your graph passes between nodes"""
    pass

graph = StateGraph(GraphState)

graph.add_node("fetch_sheet", fetch_last_row_from_sheet)
graph.add_node("get_free_day", get_next_free_day)
graph.add_node("send_emails", send_emails)

graph.set_entry_point("fetch_sheet")
graph.add_edge("fetch_sheet", "get_free_day")
graph.add_edge("get_free_day", "send_emails")
graph.add_edge("send_emails", END)

# ---------------------------
# Export compiled graph
# ---------------------------

portfolio_contact_graph = graph.compile()
