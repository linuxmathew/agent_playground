"""
Quick start
-----------


1. Copy `.env.example` to `.env` and fill values.
2. Create a Python venv and install packages:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


3. Make sure your LangGraph Cloud project has MCP integrations configured for:
- Google Sheets
- Google Calendar
- Email (SMTP or provider)


4. Deploy the graph in LangGraph Studio or ensure `GRAPH_ID` references your
deployed graph.


5. Run the API locally for testing:
python main.py


6. Trigger the agent from your frontend by POSTing to:
http://localhost:8000/trigger-agent


Notes
-----
- The code assumes the LangGraph SDK provides `LangGraphClient` with a
`run_graph(graph_id, input)` method; adapt to whatever your installed SDK
exposes.
- For production deployment, add authentication, retries, logging, and
monitoring. Consider hosting on Render, Railway, or a LangGraph Cloud SaaS if
available.
"""