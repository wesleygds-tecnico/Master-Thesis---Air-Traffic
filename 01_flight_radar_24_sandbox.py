import requests

# Define your API token and the endpoint URL
# API_TOKEN = "9e1c12f1-99ee-4e79-a3a0-efb4660acacc|78hk2tKl84pMEedoFbIw6E2h6D4MRLJ5eZtm9uka7b5fe730"
BASE_URL = "https://fr24api.flightradar24.com/api"
ENDPOINT = "/sandbox/static/airlines/AAL/light"

# Construct the full URL
url = f"{BASE_URL}{ENDPOINT}"

# Define the headers, including the Authorization header with your API token
headers = {
    # "Accept": "application/json",
    "Authorization": "Bearer 9e1c12f1-99ee-4e79-a3a0-efb4660acacc|78hk2tKl84pMEedoFbIw6E2h6D4MRLJ5eZtm9uka7b5fe730",
    "Accept-Version": "v1"
}

# Define any query parameters, if needed (optional)
params = {
    "bounds": "50.682,46.218,14.422,22.243"  # Example coordinates
}

# Make the GET request to the API
response = requests.get(url, headers=headers)#, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the JSON response
    data = response.json()
    print("Live Flight Positions:")
    print(data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)