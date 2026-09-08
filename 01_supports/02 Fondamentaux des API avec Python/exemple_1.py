import requests

response = requests.get(
    "https://api.github.com/users/python"
)

print(response.status_code)
# print(response.json())

