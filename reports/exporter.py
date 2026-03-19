import csv
import sqlite3
import os
from datetime import datetime

DB_PATH = "db/vulntracker.db"
REPORTS_DIR = "reports"

def export_to_csv():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vulnerabilities ORDER BY date_found DESC")
    rows = cursor.fetchall()
    conn.close()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{REPORTS_DIR}/vulnreport_{timestamp}.csv"

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "ID", "Package", "Version", "Vulnerability ID",
            "Description", "Fix Versions", "CVSS Score",
            "Severity", "Status", "Date Found", "Date Resolved"
        ])

        for row in rows:
            writer.writerow(row)

    print(f"Report exported to: {filename}")
    return filename

if __name__ == "__main__":
    export_to_csv()