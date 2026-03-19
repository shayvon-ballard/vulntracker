import sqlite3
from datetime import datetime

DB_PATH = "db/vulntracker.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package TEXT NOT NULL,
            version TEXT NOT NULL,
            vuln_id TEXT NOT NULL,
            description TEXT,
            fix_versions TEXT,
            cvss_score TEXT DEFAULT 'N/A',
            severity TEXT DEFAULT 'N/A',
            status TEXT DEFAULT 'open',
            date_found TEXT NOT NULL,
            date_resolved TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def save_vulnerabilities(vulns):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    saved = 0
    for v in vulns:
        cursor.execute('''
            INSERT INTO vulnerabilities 
            (package, version, vuln_id, description, fix_versions, cvss_score, severity, date_found)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            v["package"],
            v["version"],
            v["vuln_id"],
            v["description"],
            ", ".join(v["fix_versions"]),
            v.get("cvss_score", "N/A"),
            v.get("severity", "N/A"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        saved += 1
    conn.commit()
    conn.close()
    print(f"Saved {saved} vulnerabilities to database!")

def get_all_vulnerabilities():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vulnerabilities ORDER BY date_found DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
def update_status(vuln_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if new_status == "resolved":
        cursor.execute('''
            UPDATE vulnerabilities 
            SET status = ?, date_resolved = ?
            WHERE id = ?
        ''', (new_status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), vuln_id))
    else:
        cursor.execute('''
            UPDATE vulnerabilities 
            SET status = ?, date_resolved = NULL
            WHERE id = ?
        ''', (new_status, vuln_id))
    
    conn.commit()
    conn.close()
    print(f"Updated vulnerability {vuln_id} to {new_status}")