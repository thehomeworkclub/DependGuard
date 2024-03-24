import requests
import time
import keys


apikey_list = keys.keylist

apiKey = apikey_list[0]

libname = "com.google.guava:guava"
libver = "33.1.0-jre"
pckmanager = "maven"

response = requests.get(f"https://libraries.io/api/maven/${libname}/${libver}/dependencies?api_key=${apiKey}")

# Number of times to run the request
num_requests = 1

# Counter for rate limit errors
rate_limit_errors = 0

for _ in range(num_requests):
  try:
    response = requests.get(f"https://libraries.io/api/{pckmanager}/{libname}/{libver}/dependencies?api_key={apiKey}")
    # Process the response here
    data = response.json()
    description = data.get("description")
    print (description)
    # keywords = " ".join(description)
    # print(keywords)

    simlibs = requests.get(f"https://libraries.io/api/search?q={description}&api_key={apiKey}")
    simlibsdata = simlibs.json()
    simnames = data.get("name")
    print("similar libaries:" + simnames)

    print(simlibs.json())
  except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    break
  

  # Check if rate limit exceeded
  if response.status_code == 429:
    print("Rate limit exceeded, switching keys")
    rate_limit_errors += 1
    if rate_limit_errors >= len(apikey_list):
      print("All API keys have been exhausted.")
      break
    else:
      apiKey = apikey_list[rate_limit_errors]
      print(f"Switching to API key: {apiKey}")
      time.sleep(1)  # Wait for 1 second before making the next request



#GET https://libraries.io/api/search?q=grunt&api_key=YOUR_API_KEY