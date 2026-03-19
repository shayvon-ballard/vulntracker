from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

DB_PATH = "db/vulntracker.db"

def get_vulnerabilities():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vulnerabilities ORDER BY date_found DESC")
    rows = cursor.fetchall()
    conn.close()
    vulns = []
    for row in rows:
        vulns.append({
            "id": row[0],
            "package": row[1],
            "version": row[2],
            "vuln_id": row[3],
            "description": row[4],
            "fix_versions": row[5],
            "cvss_score": row[6],
            "severity": row[7],
            "status": row[8],
            "date_found": row[9]
        })
    return vulns

def get_stats(vulns):
    total = len(vulns)
    open_count = sum(1 for v in vulns if v["status"] == "open")
    resolved_count = sum(1 for v in vulns if v["status"] == "resolved")
    github_count = sum(1 for v in vulns if v["severity"] == "See GitHub Advisory")
    pypi_count = sum(1 for v in vulns if v["severity"] == "See PyPI Advisory")
    return {
        "total": total,
        "open": open_count,
        "resolved": resolved_count,
        "github": github_count,
        "pypi": pypi_count
    }

@app.route("/")
def index():
    vulns = get_vulnerabilities()
    stats = get_stats(vulns)
    return render_template("index.html", vulns=vulns, stats=stats)
@app.route("/export")
def export():
    from reports.exporter import export_to_csv
    filename = export_to_csv()
    return redirect(url_for("index"))
@app.route("/update_status", methods=["POST"])
def update_status():
    vuln_id = request.form.get("vuln_id")
    new_status = request.form.get("status")
    from db.tracker import update_status as db_update
    db_update(vuln_id, new_status)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)