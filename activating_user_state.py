import requests, json, csv

okta_domain = "https://<domain>.okta.com"
token = ""
##############################################################

url = okta_domain + "/api/v1/users?limit=2"
headers = {"Authorization": "SSWS " + token,
          "Accept": "application/json",
          "Content-Type": "application/json"}

act_users = []

def get_users(url, headers):
    r = requests.get(url, headers=headers)
    users = json.loads(r.text)

    for user in users:
        if user["status"] == "ACTIVE":
            act_users.append(user)

    print(r.headers)
    if "next" in r.headers["link"]:
        next_link = r.headers["link"].split(",")[1]
        next_link = next_link.split(">")[0][2:]
        get_users(next_link, headers)

    return act_users


def csv_users(act_users):
    with open("users.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Id", "Login", "Email", "First Name", "Last Name"])
        for user in act_users:
            uid = user["id"]
            login = user["profile"]["login"]
            email = user["profile"]["email"]
            fn = user["profile"]["firstName"]
            ln = user["profile"]["lastName"]

            usr_att = [uid, login, email, fn, ln]
            writer.writerow(usr_att)

    return


csv_users(get_users(url, headers))
print(get_users(url, headers))