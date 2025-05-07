from typing import Any
import httpx
import json
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Constants
CISCO_CVM_API_BASE = "https://api.kennasecurity.com/vulnerability_definitions"
RISK_TOKEN = os.getenv("RISK_TOKEN")

# Ensure the RISK_TOKEN is loaded
if not RISK_TOKEN:
    raise ValueError("RISK_TOKEN is not set in the environment variables.")

async def make_cisco_cvm_request(cve_id: str) -> dict[str, Any] | None:
    """Make a request to the Cisco CVM API with proper error handling."""
    headers = {
        "X-Risk-Token": RISK_TOKEN,
        "Accept": "application/json"
    }
    url = f"{CISCO_CVM_API_BASE}/{cve_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()

            # Validate the JSON structure
            if not isinstance(data, dict) or "vulnerability_definition" not in data:
                print("Error: Incomplete or invalid JSON response.")
                return None

            print("Raw API Response:", json.dumps(data, indent=2))
            return data
        except httpx.RequestError as e:
            print(f"Request error: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except ValueError as e:
            print(f"JSON decoding error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None

def format_cve_response(data: dict) -> str:
    """Format the CVE response into a readable string."""
    vuln_def = data.get("vulnerability_definition", {})
    # Ensure only valid strings are included in the join operation
    fixes = ', '.join(fix.get('url', 'N/A') for fix in vuln_def.get('fixes', []) if fix and isinstance(fix.get('url'), str))
    exploits = ', '.join(fix.get('url', 'N/A') for fix in vuln_def.get('exploits', []) if fix and isinstance(fix.get('url'), str))
    response = f"""
CVE ID: {vuln_def.get('cve_id', 'Unknown')}
Description: {vuln_def.get('description', 'No description available')}
Risk Meter Score: {round(vuln_def.get('risk_meter_score', 0), 2) if isinstance(vuln_def.get('risk_meter_score'), (int, float)) else 'N/A'}
CVSS Score: {vuln_def.get('cvss_score', 'N/A')}
CVSS v3 Score: {vuln_def.get('cvss_v3_score', 'N/A')}
Malware Exploitable: {'True' if vuln_def.get('malware_exploitable', False) else 'False'}
Active Internet Breach: {'True' if vuln_def.get('active_internet_breach', False) else 'False'}
Remote Code Execution: {'True' if vuln_def.get('remote_code_execution', False) else 'False'}
Easily Exploited: {'True' if vuln_def.get('easily_exploited', False) else 'False'}
Published At: {vuln_def.get('created_at', 'Unknown')}
Fixes: {fixes}
Exploits: {exploits}
"""
    return response

async def main():
    cve_id = "CVE-2023-23397"  # Hardcoded CVE ID
    data = await make_cisco_cvm_request(cve_id)
    if not data:
        print("Unable to fetch CVE details or no data found.")
        return
    print(format_cve_response(data))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())