import random
import sqlite3
from string import digits
import sys

db_name = "card.s3db"


def generate_number():
    number = "400000"
    for _ in range(9):
        number += random.choice(digits)

    luhn_number = [int(x) for x in number]

    for i in range(15):
        if (i + 1) % 2 != 0:
            luhn_number[i] *= 2
    for i in range(15):
        if luhn_number[i] > 9:
            luhn_number[i] -= 9
    if sum(luhn_number) % 10 == 0:
        number += '0'
    else:
        number += str(10 - (sum(luhn_number) % 10))
    return number


def generate_pin():
    pin = ""
    for _ in range(4):
        pin += random.choice(digits)
    return pin


def create_database():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0 );""")
    conn.commit()


def check_luhn(card_num: str):
    if len(card_num) != 16:
        return False
    num = [int(x) for x in card_num]
    for i in range(0, len(num) - 1, 2):
        num[i] *= 2
        if num[i] > 9:
            num[i] -= 9
    if sum(num) % 10 == 0:
        return True
    return False


class BankSystem:

    def __init__(self):

        self.database = {}
        self.balance = 0
        self.card_number = ""
        self.card_pin = ""

    def init_account(self):
        while True:
            card_num = generate_number()
            if card_num not in self.database.keys():
                self.card_number = card_num
                break
        self.card_pin = generate_pin()
        balance = self.balance
        self.database[self.card_number] = [self.card_pin, balance]

        return self.database

    def user_menu(self):
        create_database()
        while True:
            home_menu = input("1. Create an account\n2. Log into account\n0. Exit\n")
            if home_menu == "1":
                self.init_account()
                self.retrieve_from_database()
                print(f"\nYour card has been created \
                        \nYour card number:\n{self.card_number}\nYour card PIN:\n{self.card_pin}\n")
            elif home_menu == "2":
                card_number = input("\nEnter your card number:\n")
                card_pin = input("Enter your PIN:\n")
                if card_number in self.database.keys() and card_pin in self.database[card_number]:
                    print("\nYou have successfully logged in!")
                    while True:
                        submenu = input("\n1. Balance\n2. Add income\n3. Do transfer"
                                        "\n4. Close account\n5. Log out\n0. Exit\n")
                        if submenu == "1":
                            print(f"\nBalance: {self.balance}\n")
                        elif submenu == "2":
                            inp_income = int(input("\nEnter income:\n"))
                            self.database[card_number][1] += inp_income
                            self.update_balance(card_number)
                            print("Income was added!")
                        elif submenu == "3":
                            print("Transfer\n")
                            inp_number = input("Enter card number:\n")
                            if inp_number == card_number:
                                print("You can't transfer money to the same account!")
                            elif not check_luhn(inp_number):
                                print("Probably you made a mistake in the card number. Please try again!")
                            elif inp_number not in self.database.keys():
                                print("Such a card does not exist.")
                            else:
                                transfer_amount = int(input("Enter how much money you want to transfer:\n"))
                                if transfer_amount > self.database[card_number][1]:
                                    print("Not enough money!")
                                else:
                                    self.transfer(inp_number, transfer_amount)
                                    self.database[card_number][1] -= transfer_amount
                                    self.update_balance(card_number)
                                    print("Success!")
                        elif submenu == "4":
                            self.delete_account(card_number)
                            print("\nThe account has been closed!")
                        elif submenu == "5":
                            print("\nYou have successfully logged out!\n")
                        elif submenu == "0":
                            print("\nBye")
                            sys.exit()

                else:
                    print("\nWrong card number or PIN!\n")
            else:
                if home_menu == "0":
                    print("\nBye!")
                    break

    def add_to_database(self):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("INSERT INTO card VALUES (1, ?, ?, ?)", (self.card_number, self.card_pin, self.balance))
        conn.commit()

    def update_database(self):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("""INSERT INTO card (number, pin, balance)
                    VALUES (?, ?, ?)""", (self.card_number, self.card_pin, self.balance))
        conn.commit()

    def retrieve_from_database(self):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("SELECT * FROM card")
        rows = cur.fetchall()
        if len(rows) == 0:
            self.add_to_database()
        else:
            self.update_database()

    def update_balance(self, card_number):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("UPDATE card SET balance = ? WHERE number = ?", (self.database[card_number][1], card_number))
        conn.commit()

    def transfer(self, requested_number, amount: int):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (amount, requested_number))
        conn.commit()

    def delete_account(self, card_number):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("DELETE FROM card WHERE number = ?", (card_number,))
        conn.commit()


if __name__ == "__main__":
    BankSystem().user_menu()
