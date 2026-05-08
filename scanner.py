import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime

# --- NEW: Setup the Database ---
def setup_database():
    conn = sqlite3.connect('scans.db')
    cursor = conn.cursor()
    # Create a table to hold our data if it doesn't exist yet
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            scan_date TEXT,
            https_secure BOOLEAN,
            privacy_found BOOLEAN,
            cookie_found BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

# Run setup when the script starts
setup_database()
# -------------------------------

def audit_website(url):
    if not url.startswith('http'):
        url = 'https://' + url

    report = {
        "target_url": url,
        "is_secure_https": False,
        "found_privacy_policy": False,
        "found_cookie_notice": False,
        "scan_status": "Processing"
    }

    try:
        response = requests.get(url, timeout=10)
        
        if response.url.startswith('https'):
            report["is_secure_https"] = True
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            if 'privacy' in link.text.lower() or 'privacy' in link['href'].lower():
                report["found_privacy_policy"] = True
                break
                
        page_text = soup.get_text().lower() 
        if 'cookie' in page_text or 'consent' in page_text:
            report["found_cookie_notice"] = True
                
        report["scan_status"] = "Success"

        # --- NEW: Save the result to the Database ---
        conn = sqlite3.connect('scans.db')
        cursor = conn.cursor()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO history (url, scan_date, https_secure, privacy_found, cookie_found)
            VALUES (?, ?, ?, ?, ?)
        ''', (url, current_time, report["is_secure_https"], report["found_privacy_policy"], report["found_cookie_notice"]))
        
        conn.commit()
        conn.close()
        # ------------------------------------------
        
    except Exception as error:
        report["scan_status"] = f"Failed: {str(error)}"

    return report

# --- NEW: A function to get past scans ---
def get_scan_history():
    conn = sqlite3.connect('scans.db')
    cursor = conn.cursor()
    # Get the 5 most recent scans
    cursor.execute('SELECT url, scan_date, https_secure FROM history ORDER BY id DESC LIMIT 5')
    rows = cursor.fetchall()
    conn.close()
    
    # Format the data for the API
    history = []
    for row in rows:
        history.append({
            "url": row[0],
            "date": row[1],
            "passed": row[2] == 1
        })
    return history