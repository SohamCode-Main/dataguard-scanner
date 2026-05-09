import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime

# --- 1. Database Setup ---
def setup_database():
    conn = sqlite3.connect('scans.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            scan_date TEXT,
            https_secure BOOLEAN,
            privacy_found BOOLEAN,
            cookie_found BOOLEAN,
            score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

setup_database()

# --- 2. The Upgraded Scanner Engine ---
def audit_website(url):
    if not url.startswith('http'):
        url = 'https://' + url

    report = {
        "target_url": url,
        "is_secure_https": False,
        "found_privacy_policy": False,
        "found_cookie_notice": False,
        "security_headers_count": 0,
        "compliance_score": 0,
        "scan_status": "Processing"
    }

    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        
        # HTTPS Check
        if response.url.startswith('https'):
            report["is_secure_https"] = True
            
        # Content Scan
        soup = BeautifulSoup(response.text, 'html.parser')
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            if 'privacy' in link.text.lower() or 'privacy' in link['href'].lower():
                report["found_privacy_policy"] = True
                break
                
        page_text = soup.get_text().lower() 
        if 'cookie' in page_text or 'consent' in page_text:
            report["found_cookie_notice"] = True

        # Security Header Check
        headers_to_check = ['Strict-Transport-Security', 'X-Frame-Options', 'X-Content-Type-Options']
        for h in headers_to_check:
            if h in headers:
                report["security_headers_count"] += 1

        # Scoring Algorithm
        score = 0
        if report["is_secure_https"]: score += 30
        if report["found_privacy_policy"]: score += 30
        if report["found_cookie_notice"]: score += 20
        score += (report["security_headers_count"] * 6.6)
        
        report["compliance_score"] = round(min(score, 100))
        report["scan_status"] = "Success"

        # Save result to DB
        conn = sqlite3.connect('scans.db')
        cursor = conn.cursor()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO history (url, scan_date, https_secure, privacy_found, cookie_found, score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (url, current_time, report["is_secure_https"], report["found_privacy_policy"], report["found_cookie_notice"], report["compliance_score"]))
        conn.commit()
        conn.close()
        
    except Exception as error:
        report["scan_status"] = f"Failed: {str(error)}"

    return report

# --- 3. The History Function (Crucial for main.py) ---
def get_scan_history():
    conn = sqlite3.connect('scans.db')
    cursor = conn.cursor()
    cursor.execute('SELECT url, scan_date, https_secure, score FROM history ORDER BY id DESC LIMIT 5')
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "url": row[0],
            "date": row[1],
            "passed": row[2] == 1,
            "score": row[3] if row[3] is not None else 0
        })
    return history