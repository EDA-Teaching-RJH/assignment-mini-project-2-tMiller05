import re
import csv

class User:
    def __init__(self,Name,Email,Passw,Balance):
        self.Name = Name
        self.Email = Email
        self.Passw = Passw
        self.Wallet = Wallet(Balance)

class Wallet:
    def __init__(self,Balance):
        self.Balance = float(Balance)

    def deposit(self,amt):
        if amt > 0:
            self.Balance += amt
            print(f"{amt} has been deposited.")
            return True
        return False
        
    def withdraw(self,amt):
        if amt > self.Balance:
            print("Insufficient funds.")
        else:
            self.Balance =- amt
            print(f"{amt}  has been withdrawn.")



def newUser():
    print("-- Create Account --")
    Name=input("Enter Name:   ").title()

    Email=input("Enter Email:   ").lower()
    if not re.match(r".+@.+",Email):
        print("Invalid Email, Try Again.")
        return
    
    print("Password must be at least 8 characters with 1 capital Letter and 2 numbers.")
    Passw=input("Enter Password   ")
    if not re.match(r"^(?=.*[A-Z])(?=(?:.[0-9]){2,}).{8,}",Passw):
        print("Passoword not safe, try another.")
        return

    Balance = input("Enter initial balance:   ")
    if not re.match(r"^\d+(\.\d{1,2})?$",Balance):
        print("Incorrect format, use 0.00.")
        return
    
    newUser=User(Name,Email,Passw,Balance)
    with open ("Users.csv", mode="a", newline="") as file:
        Writer=csv.writer(file)
        Writer.writerow([newUser.Name, newUser.Email, newUser.Passw, newUser.Wallet.Balance])
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
    while True:
        print(f"-- Welcome {loggedIn.Name} --")
        print("1.   View balance")
        print("2.   Deposit")
        print("3.   Withdraw")
        choice = input("Choose an option.")
        if choice == "1":
            print(f"--  You currently have £{loggedIn.Wallet.Balance}  --")
        if choice == "2":
            amt=float(input("How much would you like to add?"))
            if loggedIn.Wallet.deposit(amt):
                print("Success!")
            else:
                print("Number must be positive.")
        if choice == "3":
            amt=float(input(""))

            


def main():
    while True:
        print(" Initialising program...")
        print(" --WELCOME--")
        print("1.   Sign up")
        print("2.   Log in")
        option = input("Have an account?")

        if option == "1":
            newUser()
            return False
        elif option == "2":
            loggedIn = login()
            if loggedIn:
                menu(loggedIn)
            return False
        else:
            print("That is not an option.")
            break
    

if __name__ == "__main__":
    main()