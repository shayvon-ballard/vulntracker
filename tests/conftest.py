import pytest
import sys
import os
import sqlite3
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dashboard')))

@pytest.fixture
def app():
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

    os.environ["DB_PATH"] = db_file

    import app as flask_module
    flask_module.DB_PATH = db_file

    yield flask_module.app

    os.unlink(db_file)
    del os.environ["DB_PATH"]

@pytest.fixture
def client(app):
    return app.test_client()