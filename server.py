import http.server
import socketserver
import json
from urllib.parse import urlparse

# --- Configuration ---
PORT = 8000
LOCAL_SERVER_URL = f"http://localhost:{PORT}"
ACTUAL_PIPEDREAM_URL = "https://eo98lw8093kaxpi.m.pipedream.net" 
# NOTE: The frontend's PIPEDREAM_URL constant in index.html MUST be updated to
# the LOCAL_SERVER_URL ("http://localhost:8000") for this Python server to work.
# When ready for production, switch back to the ACTUAL_PIPEDREAM_URL.
# ---------------------

class UnifiedSearchHandler(http.server.SimpleHTTPRequestHandler):
    """
    A custom HTTP request handler to handle POST requests (API calls) and
    include necessary CORS headers for local development.
    """

    def _set_headers(self, status_code=200):
        """Sets common headers, including CORS."""
        self.send_response(status_code)
        # CRITICAL for allowing the frontend (running locally) to talk to this server
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-type')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_OPTIONS(self):
        """Handles CORS pre-flight requests."""
        self._set_headers(204)

    def do_POST(self):
        """Handles POST requests, simulates AI processing, and returns JSON."""
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            # 1. Parse incoming JSON data
            request_data = json.loads(post_data.decode('utf-8'))
            query = request_data.get('query', 'No query provided.')
            print(f"Received query: '{query}'")

            # 2. --- Simulate AI & Knowledge Retrieval Logic ---
            
            # Simple simulation: response depends on the query content
            if "sales" in query.lower() or "q4" in query.lower():
                mock_summary = f"""
                AI Summary for '{query}':

                The Q4 strategy pivots on three key initiatives derived from the retrieved documents (Jira #401, Confluence Draft, and Drive Budget). The core focus is **market expansion** into the APAC region (Confluence). Resource allocation, as detailed in the Drive Budget, shows a 15% increase in marketing spend directed at digital channels. The primary bottleneck, identified in Jira #401, is the final integration of the new payment gateway, scheduled for completion by Nov 15th. All teams must align with the target KPIs defined in the Confluence document.
                """
                mock_sources = [
                    {"title": "Jira: Feature Implemention Ticket #401 (Payment Gateway)", "uri": "https://jira.example.com/T401"},
                    {"title": "Confluence: Q4 Marketing Strategy Draft", "uri": "https://confluence.example.com/Q4-Mktg-vF"},
                    {"title": "Google Drive: FY24 Quarterly Budget Planning", "uri": "https://drive.google.com/budget-FY24"},
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
                ]

            # 3. Construct the response payload (MUST match what the frontend expects)
            response_payload = {
                "status": "success",
                "summary": mock_summary.strip(),
                "sources": mock_sources
            }
            
            # 4. Send the response back to the client
            self._set_headers()
            self.wfile.write(json.dumps(response_payload).encode('utf-8'))

        except Exception as e:
            # Handle parsing or server-side errors
            print(f"Error processing request: {e}")
            error_payload = {
                "status": "error",
                "error": f"Internal Server Error: Could not process request. Detail: {str(e)}"
            }
            self._set_headers(500)
            self.wfile.write(json.dumps(error_payload).encode('utf-8'))


# --- Server Startup ---
def run_server():
    """Starts the simple HTTP server."""
    handler = UnifiedSearchHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("="*60)
        print(f"🚀 Starting Unified Search Backend SIMULATION on port {PORT}")
        print(f"🌐 Local Endpoint: {LOCAL_SERVER_URL}")
        print("-" * 60)
        print(f"Production Pipedream URL (Target): {ACTUAL_PIPEDREAM_URL}")
        print("ATTENTION: For local testing, you must update the PIPEDREAM_URL")
        print(f"in your index.html to '{LOCAL_SERVER_URL}'.")
        print("="*60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()

if __name__ == "__main__":
    run_server()