dash_space = "----------"
new_line = "\n"
tab = "    "

def display_main_menu():
    # Display main menu options
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. View Transactions")
    print("6. Exit")

def get_user_choice():
    # Get user's choice
    choice = input("Enter your choice (1-6): ")
    return choice

def create_account():
    print(new_line+dash_space+"CREATING A NEW ACCOUNT"+dash_space+new_line)
    first_name = input("enter your first name : ")
    last_name = input("enter your last name : ")
    email = input("enter your email : ")
    phone_number = input("enter your phone number : ")
    address = input("enter your address : ")
    password = input("create a password : ")

    return [(first_name, last_name, email, phone_number, address,), password]

def deposit():
    print(new_line+dash_space+"DEPOSIT"+dash_space+new_line)
    customer_id = input("enter your customer_id : ")
    password = input("enter your password : ")
    amount = float(input("enter the amount that you want to deposit : "))

    return (customer_id,password,amount,)

def widthdrawal():
    print(new_line+dash_space+"WITHDRAWAL"+dash_space+new_line)
    customer_id = input("enter your customer_id : ")
    password = input("enter your password : ")
    amount = float(input("enter the amount that you want to withdraw : "))

    return (customer_id,password,amount,)

def transfer():
    print(new_line+dash_space+"TRANSFER"+dash_space+new_line)
    source_customer_id = input("enter your customer_id : ")
    password = input("enter your password : ")
    destination_customer_id = input("enter the receivers customer_id : ")
    amount = float(input("enter the amount that you want to transfer : "))

    return (source_customer_id,password, destination_customer_id,amount,)

def view_transaction():
    print(new_line+dash_space+"TRANSACTION"+dash_space+new_line)
    source_customer_id = input("enter your customer_id : ")
    password = input("enter your password : ")

    return (source_customer_id, password)
