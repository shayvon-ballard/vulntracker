import subprocess
import json
import os
from datetime import datetime

def run_scan(api_key=None):
    print("Starting vulnerability scan...")
    print(f"Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)

    result = subprocess.run(
        ["pip-audit", "--format", "json"],
        capture_output=True,
        text=True
    )

    if result.stdout:
        data = json.loads(result.stdout)
        vulnerabilities = data.get("dependencies", [])

        found = []
        for dep in vulnerabilities:
            for vuln in dep.get("vulns", []):
                found.append({
                    "package": dep["name"],
                    "version": dep["version"],
                    "vuln_id": vuln["id"],
                    "description": vuln["description"],
                    "fix_versions": vuln.get("fix_versions", []),
                    "cvss_score": "N/A",
                    "severity": "N/A"
                })

        if api_key:
            print("Enriching vulnerabilities with NVD data...")
            from scanner.nvd_client import get_cvss_score
            for v in found:
                if v["vuln_id"].startswith("CVE"):
                    print(f"  Looking up {v['vuln_id']}...")
                    nvd_data = get_cvss_score(v["vuln_id"], api_key)
                    v["cvss_score"] = nvd_data["score"]
                    v["severity"] = nvd_data["severity"]
                elif v["vuln_id"].startswith("GHSA"):
                    v["cvss_score"] = "N/A"
                    v["severity"] = "See GitHub Advisory"
                elif v["vuln_id"].startswith("PYSEC"):
                    v["cvss_score"] = "N/A"
                    v["severity"] = "See PyPI Advisory"

        if found:
            print(f"\nFound {len(found)} vulnerabilities!")
            for v in found:
                print(f"\nPackage: {v['package']} {v['version']}")
                print(f"CVE ID: {v['vuln_id']}")
                print(f"CVSS Score: {v['cvss_score']} | Severity: {v['severity']}")
                print(f"Description: {v['description'][:100]}...")
        else:
            print("No vulnerabilities found!")

        return found

    return []

if __name__ == "__main__":
    from db.tracker import init_db, save_vulnerabilities

    api_key = os.environ.get("NVD_API_KEY")
    if not api_key:
        print("Warning: No NVD_API_KEY found, skipping enrichment...")

    init_db()
    vulns = run_scan(api_key=api_key)
    save_vulnerabilities(vulns)
