from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from scanner import audit_website, get_scan_history

app = FastAPI(title="DataGuard: GDPR Compliance Auditor")

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# --- Routes ---

@app.get("/")
def read_root():
    """Serves the frontend HTML file."""
    return FileResponse("index.html")

@app.get("/audit")
def run_scan(url: str):
    """Triggers a website audit."""
    report_data = audit_website(url)
    return report_data

@app.get("/history")
def read_history():
    """Retrieves scan history from the database."""
    recent_scans = get_scan_history()
    return {"history": recent_scans}