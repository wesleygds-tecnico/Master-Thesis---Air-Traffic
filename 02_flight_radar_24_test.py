import requests

url = "https://fr24api.flightradar24.com/api/sandbox/static/airlines/AAL/light"

headers = {
    "Authorization": "Bearer 9e1c12f1-99ee-4e79-a3a0-efb4660acacc|78hk2tKl84pMEedoFbIw6E2h6D4MRLJ5eZtm9uka7b5fe730",
    "Accept-Version": "v1"  # Add this required header
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Parse and print the JSON response
    data = response.json()
    print("Live Flight Positions:")
    print(data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)