import requests
import time
import json


apikey_list = ["53d6ec55fcbfdedb9ac6bd44ae42050c", "10b8f9c2a81b273a6c0db61fb96fb212", "7165ca9cc733d1abd00a87a930d9d714"]


apiKey = apikey_list[0]

libname = "org.apache.pulsar:pulsar-functions-worker"
libver = "2.11.3"
pckmanager = "Maven"

response = requests.get(f"https://libraries.io/api/maven/${libname}/${libver}/dependencies?api_key=${apiKey}")

# Number of times to run the request
num_requests = 1

# Counter for rate limit errors
rate_limit_errors = 0







def get_vuln_data(libname, libver, pckmanager):
  for _ in range(num_requests):
    try:
      data = {
        "version": libver,
        "package": {"name": libname, "ecosystem": pckmanager},
      }

      headers = {
        "Content-Type": "application/json"
      }

      response = requests.post("https://api.osv.dev/v1/query", json=data, headers=headers)
      response_json = response.json()
      vulns = response_json.get("vulns", [])
      vuln_data = {}

      for vuln in vulns:
          aliases = vuln.get("aliases", [])
          details = vuln.get("details", "No details available")
          affected_versions = vuln.get("affected", [{}])[0].get("versions", [])
          fixed_version_events = vuln.get("affected", [{}])[0].get("ranges", [{}])[0].get("events", [])
          fixed_version = next((event.get("fixed") for event in fixed_version_events if event.get("fixed")), "Not specified")
          severity_info = vuln.get("severity", [])
          
          for severity in severity_info:
              if severity.get("type") == "CVSS_V3":
                  score = severity.get("score")
                  cvss_score = score.split('/')[0] if score else None
                  break

          for alias in aliases:
              vuln_data[alias] = {
                  "CVSS Score": cvss_score,
                  "Details": details,
                  "Affected Versions": affected_versions,
                  "Fixed Version": fixed_version
              }

      print(vuln_data)




      print(response.json())
    except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")
      break



#GET https://libraries.io/api/search?q=grunt&api_key=YOUR_API_KEY