import requests
import time
import keys


apikey_list = keys.keylist  # List of API keys from keys.py

apiKey = apikey_list[0]  # Initialize with the first API key

# Example library information (modify as needed)
libname = "com.google.guava:guava"
libver = "33.1.0-jre"
pckmanager = "maven"

# Initial API request to get library dependencies
response = requests.get(f"https://libraries.io/api/maven/${libname}/${libver}/dependencies?api_key=${apiKey}")

# Number of times to run the request (modify as needed)
num_requests = 1

# Counter for rate limit errors
rate_limit_errors = 0

for _ in range(num_requests):
    try:
        # Make the API request to fetch dependencies
        response = requests.get(f"https://libraries.io/api/{pckmanager}/{libname}/{libver}/dependencies?api_key={apiKey}")

        # Process the response
        data = response.json()
        description = data.get("description")  # Extract library description
        print(description)

        # TODO: Implement keyword extraction or processing logic here
        # You can use the description or other data from the response to extract relevant keywords.

        # Example: Search for similar libraries based on the description
        simlibs = requests.get(f"https://libraries.io/api/search?q={description}&api_key={apiKey}")
        simlibsdata = simlibs.json()
        simnames = data.get("name")
        print("Similar libraries:" + simnames)
        print(simlibs.json())

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        break

    # Handle rate limiting
    if response.status_code == 429:
        print("Rate limit exceeded, switching keys")
        rate_limit_errors += 1
        if rate_limit_errors >= len(apikey_list):
            print("All API keys have been exhausted.")
            break
        else:
            apiKey = apikey_list[rate_limit_errors]  # Switch to the next API key
            print(f"Switching to API key: {apiKey}")
            time.sleep(1)  # Wait for 1 second before making the next request