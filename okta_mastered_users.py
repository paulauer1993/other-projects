import requests, json

token = ""

headers = {"Authorization" : "SSWS " + token,
          "Accept" : "application/json",
          "Content-Type" : "application/json"}

r = requests.get("https://<domain>.okta.com/api/v1/users", headers = headers)
req = json.loads(r.text)

usernames = []
for user in req:
    if user["credentials"]["provider"]["type"] == "OKTA":
        usernames.append(user["profile"]["login"])

print(usernames)