import requests, random, string, json

token = ""

headers = {"Authorization" : "SSWS " + token,
          "Accept" : "application/json",
          "Content-Type" : "application/json"}

prm = {"activate" : True}

url = "https://<domain>.okta.com"

words = requests.get("http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain")
words = words.text.splitlines()

def main(words):
    number = int(input("How many users: "))
    domain = input("Domain: ")
    for n in range(number):
        fn = random.choice(words).lower()
        ln = random.choice(words).lower()
        print(createUser(fn, ln, url, headers, prm, domain))

def createUser(fn, ln, url, headers, prm, domain):
    body = {"profile": {
        "firstName":f"{fn}".capitalize(),
        "lastName":f"{ln}".capitalize(),
        "login":f"{fn}.{ln}@{domain}",
        "email":f"{fn}.{ln}@{domain}"},
     "credentials":{
         "password":{"value":"".join([random.choice(string.ascii_letters) + random.choice(string.digits) + random.choice(string.punctuation) for n in range(9)])}
     }
        }

    psw = body["credentials"]["password"]["value"]
    login = body["profile"]["login"]
    fn = body["profile"]["firstName"]
    ln = body["profile"]["lastName"]

    create = requests.post(f"{url}/api/v1/users", headers=headers, params=prm, data=json.dumps(body))
    print(create.content)
    return f"{fn} {ln}, with login and email: {login} was created with password: {psw}."

main(words)