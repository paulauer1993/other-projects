import requests, json

token = ""

headers = {"Authorization" : "SSWS " + token,
          "Accept" : "application/json",
          "Content-Type" : "application/json"}

def main():
    login = input("User's login: ")
    id = getUser(login)["id"]
    fn = getUser(login)["profile"]["firstName"]
    ln = getUser(login)["profile"]["lastName"]
    if getUser(login)["status"] != "DEPROVISIONED":
        choice = input("Deactivate user and then delete?\n(y/n)")
        if choice == "y":
            deactivateUser(id)
            deleteUser(id)
            if deleteUser(id):
                print(f"{fn} {ln} was deleted.")
        else:
            main()
    else:
        choice = input("Are you sure?\n(y/n)")
        if choice == "y":
            deleteUser(id)
            if deleteUser(id):
                print(f"{fn} {ln} was deleted.")
        else:
            main()

def getUser(login):
    r = requests.get(f"https://<subdomain>.okta.com/api/v1/users?filter=profile.login%20eq%20%22{login}%22", headers = headers)
    req = json.loads(r.text)
    return req[0]

def deactivateUser(id):
    r = requests.post(f"https://<subdomain>.okta.com/api/v1/users/{id}/lifecycle/deactivate", headers=headers)
    return r.status_code

def deleteUser(id):
    r = requests.delete(f"https://<subdomain>.okta.com/api/v1/users/{id}", headers=headers)
    return r.status_code

main()