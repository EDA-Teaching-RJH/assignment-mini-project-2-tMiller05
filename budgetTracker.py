import re
import csv

class User:
    def __init__(self,Name,Email,Passw,Balance):
        self.Name = Name
        self.Email = Email
        self.Pass = Passw
        self.Wallet = Wallet(Balance)

class Wallet:
    def __init__(self,Balance):
        self.Balance = float(Balance)

    def addFunds(self,Balance):
        if amount > 0:
            self.Balance += amount
            return True
        return False



def newUser():
    print("-- Create Account --")
    Name=input("Enter Name:   ").title()

    Email=input("Enter Email:   ")
    if not re.match(r".+@.+",Email):
        print("Invalid Email, Try Again.")
        return
    
    print("Password must be at least 8 characters with 1 capital Letter and 2 numbers.")
    Passw=input("Enter Password   ")
    if not re.match(r"^(?=.*[A-Z])(?=(?:.[0-9]){2,}.{8,}$)",Passw):
        print("Passoword not safe, try another.")
        return

    Balance = input("Enter initial balance:   ")
    if not re.match(r"^\d+(\.\d{1,2})?$",Balance):
        print("Incorrect format, use 0.00.")
        return
    
    newUser=User(Name,Email,Passw,Balance)
    with open ("Users.csv", mode="a", newline="") as file:
        Writer=csv.writer(file)
        Writer.writerow([newUser.Name, newUser.Email, newUser.Pass, newUser.Balance])
    print(f"User {Name} has been added successfully.")

def login():
    
    print("-- Login --")
    emailInput=input("Enter Email   ")
    passInput=input("Enter Password   ")

    with open ("Users.csv", mode="r", newline="") as file:
        reader=csv.reader(file)
        next(reader)
        for row in reader:
            if row[1]==emailInput and row[2]==passInput:
                print("Login Successful")
                return User(row[0], row[1], row[2],row[3])
    print("invald credentials.")
    return None

def menu(loggedIn):
    print(-- "Welcome {loggedIn.Name} --")
    print("Choose an option:")
    print("1.   View accounts")
    print("2.   Deposit")
    print("3.   Withdraw")
