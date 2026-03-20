import re
import csv

class User:
    def __init__(self,Name,Email,Passw,Balance):
        self.Name = Name
        self.Email = Email
        self.Passw = Passw
        self.Wallet = Wallet(Balance)
class PremUser(User):
    cashbackRate = 0.05
    overdraft = 200.00
    def __init__(self,Name,Email,Passw,Balance):
        super().__init__(Name,Email,Passw,Balance)
        self.isPremium = True
        self.cashbackEarnt = 0.0
    def withdraw(self, amt):
        if amt<= 0:
            print("amount must be positive")
            return False
        if amt > self.Wallet.Balance + self.overdraft:
            print("Exceeds overdraft limit.")
            return False
        self.Wallet.Balance-=amt
        cashback=round(amt*self.cashbackRate,2)
        self.cashbackEarnt+=cashback
        print(f"£{amt} withdrawn, you have earned £{self.cashbackEarnt} cashback!")
        return True
    def redeem(self):
        if self.cashbackEarnt <= 0:
            print("There is no cashback to redeem")
            return
        self.Wallet.deposit(self.cashbackEarnt)
        

class Wallet:
    def __init__(self,Balance):
        self.Balance = float(Balance)

    def deposit(self,amt):
        if amt > 0:
            self.Balance += amt
            print(f"{amt} has been deposited.")
            return True
        
        
    def withdraw(self,amt):
        currentBalance = self.Balance
        if amt > self.Balance:
            print("Insufficient funds.")
        else:
            self.Balance = currentBalance - amt
            print(f"{amt}  has been withdrawn.")
            return True



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
    Prem = input("Premium account? Y/N     ").upper()

    Balance = input("Enter initial balance:   ")
    if not re.match(r"^\d+(\.\d{1,2})?$",Balance):
        print("Incorrect format, use 0.00.")
        return
    
    if Prem == "Y":
        newUser=PremUser(Name,Email,Passw,Balance)
    else:
        newUser=User(Name,Email,Passw,Balance)
    with open ("Users.csv", mode="a", newline="") as file:
        Writer=csv.writer(file)
        Writer.writerow([newUser.Name, newUser.Email, newUser.Passw, newUser.Wallet.Balance, newUser.isPremium])
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
                if row[4] == "T":
                    return PremUser(row[0],row[1], row[2], row[3])
                else:
                    return User(row[0], row[1], row[2],row[3])
    print("invald credentials.")
    return None

def changeBalance(loggedIn):
    rows = []
    try:
        with open ("Users.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)
    except FileNotFoundError :
        print("File not found.")
        return
    for row in rows:
        if row[1] == loggedIn.Email:
            row[3] = f"{loggedIn.Wallet.Balance:.2f}"
            break
    with open ("Users.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)
            

def menu(loggedIn):
    while True:
        print(f"-- Welcome {loggedIn.Name} --")
        print("1.   View balance")
        print("2.   Deposit")
        print("3.   Withdraw")
        print("4.   Exit")
        if isinstance(loggedIn, PremUser):
            print("5.   Redeem Cashback")

        choice = input("Choose an option.")
        if choice == "1":
            print(f"--  You currently have £{loggedIn.Wallet.Balance}  --")
        elif choice == "2":
            amt=float(input("-- How much would you like to add? --"))
            if loggedIn.Wallet.deposit(amt):
                print("Success!")
                changeBalance(loggedIn)
                
            else:
                print("Number must be positive.")
        elif choice == "3":
            amt=float(input("-- How much would you like to take out? --"))
            if loggedIn.withdraw(amt):
                print("-- Success! --")
                changeBalance(loggedIn)
                
        elif choice =="4":
            exit=input("    You wish to quit?   Y/N").upper()
            if exit =="Y":
                break
        
        elif choice == "5":
                if isinstance(loggedIn, PremUser):
                    loggedIn.redeem()
                    changeBalance(loggedIn)
                else:
                    print("That is not an option")
        else:
            print("That is not an option")
            

            


def main():
    while True:
        print(" Initialising program...")
        print(" --WELCOME--")
        print("1.   Sign up")
        print("2.   Log in")
        print("3.   Cancel")
        option = input("Have an account?")

        if option == "1":
            newUser()
            return False
        elif option == "2":
            loggedIn = login()
            if loggedIn:
                menu(loggedIn)
            return False
        elif option == "3":
            print("Closing Program...")
            break
        else:
            print("That is not an option.")
            
    

if __name__ == "__main__":
    main()