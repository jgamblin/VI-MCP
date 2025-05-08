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

async def get_score_history(cve_id: str) -> dict[str, Any] | None:
    """Fetch the risk meter score history for a specific CVE."""
    headers = {
        "X-Risk-Token": RISK_TOKEN,
        "Accept": "application/json"
    }
    url = f"{CISCO_CVM_API_BASE}/history?cves={cve_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()

            # Validate the JSON structure
            if not isinstance(data, dict) or cve_id not in data:
                print("Error: Incomplete or invalid JSON response.")
                return None

            return data[cve_id]
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
    
    # Safely handle boolean values and ensure they are displayed as 'True' or 'False'
    def format_boolean(value):
        return 'True' if value else 'False'

    response = f"""
CVE ID: {vuln_def.get('cve_id', 'Unknown')}
Description: {vuln_def.get('description', 'No description available')}
CVSS V3 Score: {vuln_def.get('cvss_v3_score', 'N/A')}
Cisco Risk Score: {round(vuln_def.get('risk_meter_score', 0), 2) if isinstance(vuln_def.get('risk_meter_score'), (int, float)) else 'N/A'}
Malware Exploitable: {format_boolean(vuln_def.get('malware_exploitable', False))}
Active Internet Breach: {format_boolean(vuln_def.get('active_internet_breach', False))}
Remote Code Execution: {format_boolean(vuln_def.get('remote_code_execution', False))}
Easily Exploited: {format_boolean(vuln_def.get('easily_exploitable', False))}
Published At: {vuln_def.get('created_at', 'Unknown')}
Fixes: {fixes}
Exploits: {exploits}
"""
    return response

def format_score_history(history: list[dict]) -> str:
    """Format the risk meter score history into a readable string."""
    if not history:
        return "No score history available."
    formatted_history = "\n".join(
        f"Changed At: {entry['changed_at']}, From: {entry['from']}, To: {entry['to']}"
        for entry in history
    )
    return formatted_history

async def main():
    cve_id = "CVE-2023-35078"  # Updated test CVE ID
    data = await make_cisco_cvm_request(cve_id)
    if not data:
        print("Unable to fetch CVE details or no data found.")
        return

    history_data = await get_score_history(cve_id)
    score_history = format_score_history(history_data.get("risk_meter_score_history", [])) if history_data else "No score history available."

    print(f"{format_cve_response(data)}\nScore History:\n{score_history}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())