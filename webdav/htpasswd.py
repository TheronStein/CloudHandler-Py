import bcrypt
from getpass import getpass

def create_htpasswd(username, password):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return f"{username}:{password_hash.decode('utf-8')}"

if __name__ == "__main__":
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    htpasswd_entry = create_htpasswd(username, password)
    with open("/etc/nginx/.htpasswd", "a") as f:
        f.write(htpasswd_entry + "\n")
    print(f"User {username} added to /etc/nginx/.htpasswd")