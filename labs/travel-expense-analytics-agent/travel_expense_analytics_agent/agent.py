from google.adk.agents.llm_agent import Agent
from .tools import alloydb_expense_analytics, gcs_expense_processor

root_agent = Agent(
    model="gemini-3.6-flash",
    name="travel_expense_analytics_agent",
    description="Travel expense analytics agent that processes GCS expense receipts and executes AlloyDB structured expense analytics.",
    instruction=(
        "You are a travel expense analytics assistant. "
        "You have two tools available:\n"
        "1. `gcs_expense_processor`: Processes raw expense document files from Cloud Storage.\n"
        "2. `alloydb_expense_analytics`: Connects to AlloyDB PostgreSQL to execute SQL analytics on travel_expenses, "
        "aggregating 2025 expenses by team_name and month with SUM(amount) AS total_amount_usd.\n\n"
        "When requested to aggregate overall travel expenses for 2025 grouped by team and month, "
        "call `alloydb_expense_analytics(year=2025)` and present the results in a clean, beautifully formatted Markdown summary table "
        "with columns: | Team Name | Month | Total Amount (USD) |."
    ),
    tools=[gcs_expense_processor, alloydb_expense_analytics]
)
