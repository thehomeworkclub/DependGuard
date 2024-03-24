import requests
import re  # Import the regular expressions module

def get_cvss_score_from_nvd(cve_id):
    """
    Fetches the CVSS score for a given CVE ID from the NVD database by searching the response text.
    """
    nvd_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveID={cve_id}"
    try:
        response = requests.get(nvd_url)
        
        if response.status_code == 200:
            response_text = response.text
            # Use a regular expression to find "baseScore" followed by a number
            match = re.search(r'"baseScore"\s*:\s*([0-9.]+)', response_text)

                

            if match:
                cvss_score = match.group(1)  # The first capturing group contains the number
                print(f"Found CVSS Score: {cvss_score}")
                return cvss_score
            else:
                print(f"CVSS Score not found for CVE ID {cve_id}.")
                return None
        else:
            print(f"Failed to fetch data for CVE ID {cve_id}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching CVSS score for {cve_id}: {e}")
        return None


def get_vuln_data(libname, libver, pckmanager):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "version": libver,
        "package": {"name": libname, "ecosystem": pckmanager},
    }

    try:
        response = requests.post("https://api.osv.dev/v1/query", json=data, headers=headers)
        response_json = response.json()
        vulns = response_json.get("vulns", [])
        vuln_data = []

        for vuln in vulns:
            aliases = vuln.get("aliases", [])
            details = vuln.get("details", "No details available")
            affected_versions = vuln.get("affected", [{}])[0].get("versions", [])
            fixed_version_events = vuln.get("affected", [{}])[0].get("ranges", [{}])[0].get("events", [])
            fixed_version = next((event.get("fixed") for event in fixed_version_events if event.get("fixed")), "Not specified")

            # Attempt to find a CVSS score in the document
            cvss_score = None
            for alias in aliases:
                if alias.startswith("CVE-"):
                    cvss_score = get_cvss_score_from_nvd(alias)
                    if cvss_score is not None:
                        break  # Stop searching if we've found a score

            vuln_data.append({
              "id": vuln.get("id", "Unknown"),
              "CVSS Score": cvss_score,
              "Details": details,
              "Affected Versions": affected_versions,
              "Fixed Version": fixed_version
            })
            print(type(vuln_data))
        return vuln_data
      


    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example call to the function with dummy data
#get_vuln_data("jupyter-server-proxy", "4.0.0", "PyPI")
