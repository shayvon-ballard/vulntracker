import requests
import time

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def get_cvss_score(vuln_id, api_key):
    headers = {"apiKey": api_key}
    params = {"cveId": vuln_id}

    try:
        response = requests.get(NVD_API_URL, headers=headers, params=params)
        time.sleep(1)

        if response.status_code == 200:
            data = response.json()
            vulnerabilities = data.get("vulnerabilities", [])

            if vulnerabilities:
                cve = vulnerabilities[0].get("cve", {})
                metrics = cve.get("metrics", {})

                cvss_data = (
                    metrics.get("cvssMetricV31", [{}])[0].get("cvssData", {})
                    or metrics.get("cvssMetricV30", [{}])[0].get("cvssData", {})
                    or metrics.get("cvssMetricV2", [{}])[0].get("cvssData", {})
                )

                score = cvss_data.get("baseScore", "N/A")
                severity = cvss_data.get("baseSeverity", "N/A")

                return {"score": score, "severity": severity}

    except Exception as e:
        print(f"Error fetching {vuln_id}: {e}")

    return {"score": "N/A", "severity": "N/A"}