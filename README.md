# VulnTracker 🔐
A Python-based vulnerability management tool that scans environments for known security vulnerabilities, enriches findings with NVD API data, and tracks remediation through a web dashboard.

## Features
- Automated vulnerability scanning using pip-audit
- NVD API integration for CVE enrichment and CVSS scoring
- SQLite database for persistent vulnerability tracking
- Web dashboard with real-time vulnerability visualization
- Remediation workflow tracking (Open, In Progress, Resolved)
- CSV report export for management reporting

## Tech Stack
- Python 3
- Flask
- SQLite
- pip-audit
- NVD API (NIST National Vulnerability Database)

## Project Structure
```
vulntracker/
├── scanner/
│   ├── pip_scanner.py      # Core vulnerability scanner
│   └── nvd_client.py       # NVD API integration
├── db/
│   └── tracker.py          # Database operations
├── dashboard/
│   ├── app.py              # Flask web application
│   └── templates/
│       └── index.html      # Dashboard UI
├── reports/
│   └── exporter.py         # CSV report generation
└── requirements.txt
```

## Setup
```bash
# Clone the repository
git clone https://github.com/Shayvon-ballard/vulntracker.git
cd vulntracker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your NVD API key
export NVD_API_KEY=your_api_key_here
# Get a free key at: https://nvd.nist.gov/developers/request-an-api-key
```

## Usage

### Run a vulnerability scan
```bash
export PYTHONPATH=/path/to/vulntracker
python3 scanner/pip_scanner.py
```

### Launch the dashboard
```bash
python3 dashboard/app.py
```
Then open your browser at http://127.0.0.1:5000

## Dashboard
The web dashboard provides:
- Summary cards showing total vulnerabilities and open issues
- Color coded severity badges for GitHub and PyPI advisories
- Fix version recommendations for each vulnerability
- One click remediation status updates
- CSV export for management reporting

## Screenshots
![Dashboard](screenshots/08_vulntracker_dashboard_final.png)
![CSV Report](screenshots/10_csv_export_report.png)

## Author
ShayVon Ballard
- GitHub: https://github.com/Shayvon-ballard
