import random

class Customer:
    def __init__(self,name,phone,address,customer_id):
        self.name = name
        self.phone = phone
        self.address = address
        self.customer_id = customer_id
    
    def display(self):
        print("Name :",self.name)
        print("Phone :",self.phone)
        print("Address :",self.address)
        print("Customer ID :",self.customer_id)

class Account:
    def __init__(self,account_num,customer_id,account_type,balance):
        self.account_num = account_num
        self.customer_id = customer_id
        self.account_type = account_type
        self.balance = balance
    
    def debit(self):
        amount = int(input("Enter withdrawal amount : "))
        if amount <= 0:
            print("Amount must be positive")
            return 0
        if amount > self.balance:
            print("Insufficient Balance")
            return 0    
        self.balance -= amount
        print("Amount Debited :",amount)
        print("Available Balance :",self.check_balance())
        return amount

    def credit(self):
        amount = int(input("Enter deposit amount : "))
        if amount <= 0:
            print("Amount must be positive")
            return 0
        self.balance += amount
        print("Amount Credited :",amount)
        print("Available Balance :",self.check_balance())
        return amount   

    def check_balance(self):
        return self.balance

class Transaction:
    def __init__(self,transaction_id,account_num,type,amount):
        self.transaction_id = transaction_id
        self.account_num = account_num
        self.type = type
        self.amount = amount
    
    def __str__(self):
        return f"{self.transaction_id} | {self.type} | {self.amount}"
    
class Bank:
    def __init__(self,customers = None,accounts = None,transactions = None):   
        if customers == None:
            self.customers = []
        else:
            self.customers = customers

        if accounts == None:
            self.accounts = []
        else:
            self.accounts = accounts

        if transactions == None:
            self.transactions = []
        else:
            self.transactions = transactions

    def create_customer(self):
        name = input("Enter Name : ")
        phone = input("Enter Phone Number : ")
        address = input("Enter Address : ")
        customer_id = random.randint(10**5,(10**6) - 1)
        while customer_id in [Customer.customer_id for Customer in self.customers]:
            customer_id = random.randint(10**5,(10**6) - 1)
        if not (len(phone) == 10 and phone.isdigit()):
            raise ValueError("Invalid Phone Number")
        new_customer = Customer(name,phone,address,customer_id)
        self.customers.append(new_customer)
        self.save_customer()
        print("Customer Profile Created Successfully. Your Customer ID is :",customer_id)
        
    def open_account(self):
        if(input("Do you have a customer ID? (y/n) : ") == 'y'):
            customer_id = int(input("Enter Customer ID : "))
            if(customer_id not in [Customer.customer_id for Customer in self.customers]):
                raise ValueError("Customer ID not found")
            else:
                account_type = input("Enter Account Type (Savings/Current) : ")
                initial_deposit = int(input("Enter Initial Deposit Amount : "))
                if initial_deposit <= 0:
                    raise ValueError("Initial Deposit cannot be negative")
                account_num = random.randint(10**11,(10**12) - 1)
                while account_num in [Account.account_num for Account in self.accounts]:
                    account_num = random.randint(10**11,(10**12) - 1)
                new_account = Account(account_num,customer_id,account_type,initial_deposit)
                self.accounts.append(new_account)
        else:
            print("Please create a customer profile first.")
            self.create_customer()
            self.open_account()
        self.save_accounts()
        print("Account Opened Successfully. Your Account Number is :",account_num)

    def find_account(self,account_num):
        for account in self.accounts:
            if account.account_num == account_num:
                return account
        return None
    
    def perform_transaction(self):
        account_num = int(input("Enter Account Number : "))
        account = self.find_account(account_num)
        if account is None:
            print("Account not found.")
            return
        transaction_id = random.randint(10**6,(10**7) - 1)
        transaction_type = input("Enter Transaction Type (debit/credit) : ")
        if transaction_type not in ['debit','credit']:
            print("Invalid Transaction Type.")
            return
        if transaction_type == 'debit':
           amount =  account.debit()
           if amount <= 0:
               return
        elif transaction_type == 'credit':
           amount =  account.credit()
        transaction = Transaction(transaction_id,account_num,transaction_type,amount)
        self.transactions.append(transaction)
        self.save_transactions()
        print("Transaction Successful. Transaction ID is :",transaction_id)

    def balance_enquiry(self):
        account_num = int(input("Enter Account Number : "))
        account = self.find_account(account_num)
        if account is None:
            print("Account not found.")
            return
        print("Available Balance :",account.check_balance())

    def save_customer(self):
        with open("customers.txt","w") as f:
            for customer in self.customers:
                f.write(f"{customer.name},{customer.phone},{customer.address},{customer.customer_id}\n")
    
    def save_accounts(self):
        with open("accounts.txt","w") as f:
            for account in self.accounts:
                f.write(f"{account.account_num},{account.customer_id},{account.account_type},{account.balance}\n")
    
    def save_transactions(self):
        with open("transactions.txt","w") as f:
            for transaction in self.transactions:
                f.write(f"{transaction.transaction_id},{transaction.account_num},{transaction.type},{transaction.amount}\n")
    
    def load_customers(self):
        try:
            with open("customers.txt","r") as f:
                for line in f:
                    name,phone,address,customer_id = line.strip().split(",")
                    customer = Customer(name,phone,address,int(customer_id))
                    self.customers.append(customer)
        except FileNotFoundError:
            pass
    
    def load_accounts(self):
        try:
            with open("accounts.txt","r") as f:
                for line in f:
                    account_num,customer_id,account_type,balance = line.strip().split(",")
                    account = Account(int(account_num),int(customer_id),account_type,int(balance))
                    self.accounts.append(account)
        except FileNotFoundError:
            pass        

    def load_transactions(self):
        try:
            with open("transactions.txt","r") as f:
                for line in f:
                    transaction_id,account_num,type,amount = line.strip().split(",")
                    transaction = Transaction(int(transaction_id),int(account_num),type,int(amount))
                    self.transactions.append(transaction)
        except FileNotFoundError:
            pass
try:
    b = Bank()
    b.load_customers()
    b.load_accounts()
    b.load_transactions()
    while True:
        print("\n--- Bank Management System ---")
        print("1. Create Customer Profile")
        print("2. Open Account")
        print("3. Perform Transaction")
        print("4. Balance Enquiry")
        print("5. Exit")
        choice = int(input("Enter your choice : "))
        if choice == 1:
            b.create_customer()
        elif choice == 2:
            b.open_account()
        elif choice == 3:
            b.perform_transaction()
        elif choice == 4:
            b.balance_enquiry()
        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid Choice. Please try again.")

except ValueError:
    print("Enter Valid Value!!!")