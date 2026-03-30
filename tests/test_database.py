import pytest
import sqlite3
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def test_db():
    # Creates a temporary database file that gets deleted after each test
    db_file = tempfile.mktemp(suffix=".db")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE vulnerabilities (
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
    yield db_file
    os.unlink(db_file)

def test_insert_vulnerability(test_db):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vulnerabilities
        (package, version, vuln_id, description, fix_versions, cvss_score, severity, date_found)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ("requests", "2.25.0", "GHSA-test-1234", "Test vuln", "2.26.0", "7.5", "HIGH", "2024-01-01"))
    conn.commit()
    cursor.execute("SELECT * FROM vulnerabilities")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) == 1
    assert rows[0][1] == "requests"

def test_default_status_is_open(test_db):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vulnerabilities
        (package, version, vuln_id, description, fix_versions, date_found)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("flask", "2.0.0", "GHSA-test-5678", "Another vuln", "2.1.0", "2024-01-01"))
    conn.commit()
    cursor.execute("SELECT status FROM vulnerabilities WHERE package = 'flask'")
    row = cursor.fetchone()
    conn.close()
    assert row[0] == "open"

def test_update_status_to_resolved(test_db):
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vulnerabilities
        (package, version, vuln_id, description, fix_versions, date_found)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("django", "3.0.0", "GHSA-test-9999", "Django vuln", "3.1.0", "2024-01-01"))
    conn.commit()
    cursor.execute("UPDATE vulnerabilities SET status = 'resolved' WHERE package = 'django'")
    conn.commit()
    cursor.execute("SELECT status FROM vulnerabilities WHERE package = 'django'")
    row = cursor.fetchone()
    conn.close()
    assert row[0] == "resolved"