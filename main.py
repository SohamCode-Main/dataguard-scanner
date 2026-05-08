from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scanner import get_scan_history

app = FastAPI(title="DataGuard: GDPR Compliance Auditor")

# --- NEW: CORS Configuration ---
# This tells the API it is safe to talk to our HTML webpage
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows any frontend to connect during testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------

@app.get("/")
def read_root():
    return {"status": "Online", "message": "DataGuard API"}

@app.get("/audit")
def run_scan(url: str):
    report_data = audit_website(url)
    return report_data
from scanner import audit_website, get_scan_history # <-- Update your import at the top to include get_scan_history

# NEW Route: Get History
@app.get("/history")
def read_history():
    recent_scans = get_scan_history()
    return {"history": recent_scans}