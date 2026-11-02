class BankAccount:
    def __init__(self, account_holder, balance=0.0):
        self.account_holder = account_holder
        self.__balance = balance  # Encapsulated account balance
 
    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be greater than zero.")
        else:
            self.__balance += amount
            print(f"Deposited: Rs. {amount:.2f}")
 
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
        elif amount > self.__balance:
            print("Insufficient balance.")
        else:
            self.__balance -= amount
            print(f"Withdrawn: Rs. {amount:.2f}")
 
    def check_balance(self):
        print(f"Account holder: {self.account_holder}")
        print(f"Available balance: Rs. {self.__balance:.2f}")
 
 
def main():
    account = BankAccount("Mathavan", 1000.00)
    account.check_balance()
    account.deposit(500)
    account.withdraw(200)
    account.withdraw(2000)
    account.check_balance()
 
 
if __name__ == "__main__":
    main()
