from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

# Initialize the FastAPI app
app = FastAPI()

# Configuration for CORS (Allows the Vercel frontend to talk to this function)
origins = [
    "*", # Allow all origins for simplicity in Vercel deployment
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the expected request body structure
class QueryRequest(BaseModel):
    query: str

# Define the API endpoint that will handle the search query
@app.post("/api/search")
async def search_endpoint(request: QueryRequest):
    """
    Handles POST requests, simulates AI processing, and returns JSON.
    """
    query = request.query
    
    # Simulate a small delay to mimic a real API call (Latency simulation)
    time.sleep(1.0) 

    # --- Simulate AI & Knowledge Retrieval Logic ---
    
    if "sales" in query.lower() or "q4" in query.lower():
        mock_summary = f"""
AI Summary for '{query}':

The Q4 strategy pivots on three key initiatives derived from the retrieved documents (Jira #401, Confluence Draft, and Drive Budget). The core focus is **market expansion** into the APAC region (Confluence). Resource allocation, as detailed in the Drive Budget, shows a 15% increase in marketing spend directed at digital channels. The primary bottleneck, identified in Jira #401, is the final integration of the new payment gateway, scheduled for completion by Nov 15th. All teams must align with the target KPIs defined in the Confluence document.
"""
        mock_sources = [
            {"title": "Jira: Feature Implemention Ticket #401 (Payment Gateway)", "uri": "https://jira.example.com/T401"},
            {"title": "Confluence: Q4 Marketing Strategy Draft", "uri": "https://confluence.example.com/Q4-Mktg-vF"},
            {"title": "Google Drive: FY24 Quarterly Budget Planning", "uri": "https://drive.google.com/budget-FY24"},
            {"title": "SharePoint: Sales Training Material V5", "uri": "https://sharepoint.example.com/Sales-V5"},
            {"title": "GitHub: Sales Funnel API Documentation", "uri": "https://github.com/api-docs/sales"},
            {"title": "Jira: Follow-up Task for Q4 Budget", "uri": "https://jira.example.com/T402"},
            {"title": "Confluence: Marketing Team Roster", "uri": "https://confluence.example.com/team-roster"},
        ]
    elif "github" in query.lower() or "code" in query.lower():
         mock_summary = f"""
AI Summary for '{query}':

The requested code analysis (based on the GitHub PR and backend service docs) indicates the microservice architecture utilizes Python's FastAPI framework for high concurrency. The most recent Pull Request (v2) introduces an optimized caching layer using Redis, significantly reducing latency by 40%. Engineers must review the updated service documentation before deploying to staging to ensure proper logging configuration.
"""
         mock_sources = [
            {"title": "GitHub: Backend Service v2 Pull Request", "uri": "https://github.com/repo/v2-pr"},
            {"title": "Confluence: Backend Service Documentation", "uri": "https://confluence.example.com/Backend-Docs"},
            {"title": "Jira: Performance Enhancement Epic #120", "uri": "https://jira.example.com/E120"},
            {"title": "GitHub: Readme File - Installation Guide", "uri": "https://github.com/repo/readme"},
            {"title": "Google Drive: Architecture Diagram (v2)", "uri": "https://drive.google.com/arch-v2"},
         ]
    else:
        mock_summary = f"""
AI Summary for '{query}':

The search successfully retrieved multiple artifacts across various platforms related to your general query. The overall context suggests ongoing effort in documentation standardization and cross-team communication improvement. Please refine your query for a more focused and actionable summary.
"""
        mock_sources = [
            {"title": "Jira: General Documentation Cleanup Project", "uri": "https://jira.example.com/DCP-1"},
            {"title": "SharePoint: Cross-Departmental Communication Protocol", "uri": "https://sharepoint.example.com/Comms"},
            {"title": "Confluence: Team Onboarding Checklist 2024", "uri": "https://confluence.example.com/onboarding-24"},
            {"title": "Jira: Quarterly Review Task List", "uri": "https://jira.example.com/QR-Task"},
        ]

    # Construct the final response payload
    response_payload = {
        "status": "success",
        "summary": mock_summary.strip(),
        "sources": mock_sources
    }

    return response_payload