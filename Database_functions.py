import mysql.connector
import sample_data

def connect_to_database(_host, _user, _password, _database):
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host= _host,
            user= _user,
            password= _password,
            database= _database
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def execute_query(connection, query, data=None):
    """Execute a query on the MySQL database."""
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)

        connection.commit()
        return cursor  # Return the cursor for further processing

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def close_connection(connection):
    """Close the connection to the MySQL database."""
    try:
        if connection.is_connected():
            connection.close()
            print("Connection closed.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def authentication_check(_connection, customer_id, password):
    # Query to verify customer credentials
    verify_credentials_query = """
        SELECT user_authentication.password
        FROM user_authentication
        WHERE user_authentication.customer_id = %s;
    """
    cursor = _connection.cursor()
    cursor.execute(verify_credentials_query, (customer_id,))

    # Check if the customer exists and the password is correct
    row = cursor.fetchall()

    if row and row[0][0] == password:
        return True  # Authentication successful
    else:
        return False  # Authentication failed

def create_new_account(_connection, user_data, password):
    insert_new_customer_data_query = """
        INSERT INTO customer 
            (first_name, last_name, email, phone_number, address, balance) 
        VALUES (%s, %s, %s, %s, %s, 0);
    """
    execute_query(_connection, insert_new_customer_data_query, user_data)

    cursor = _connection.cursor()
    cursor.execute("SELECT MAX(customer_id) AS maximum FROM customer") 
  
    result = cursor.fetchall() 
    
    customer_id = 1

    for i in result: 
        customer_id = i[0]

    insert_new_user_authentication_data_query = """
        INSERT INTO user_authentication 
            (customer_id, password) 
        VALUES (%s, %s);
    """
    execute_query(_connection, insert_new_user_authentication_data_query, (customer_id, password))
    print("ACCOUNT HAS BEEN CREATED SUCCESSFULLY")

def deposit(_connection, customer_id, password, amount):
    #Verify customer credentials
    if not authentication_check(_connection, customer_id, password):
        print("Invalid credentials. Unable to perform withdrawal.")
        return
    
    # Customer credentials are valid, proceed with the deposit
    try:
        #Update customer balance
        update_balance_query = """
            UPDATE customer
            SET balance = balance + %s
            WHERE customer_id = %s;
        """
        execute_query(_connection, update_balance_query, (amount, customer_id))

        #record the transaction
        insert_transaction_query = """
            insert into transaction () values ();
        """
        cursor = _connection.cursor()
        cursor.execute(insert_transaction_query)

        transaction_id_query = "SELECT LAST_INSERT_ID() AS transaction_id;"
        cursor.execute(transaction_id_query)

        transaction_id = cursor.fetchall()[0][0]
        #Record the deposit
        insert_deposit_query = """
            INSERT INTO deposit 
                (transaction_id,customer_id, amount) 
            VALUES (%s, %s, %s);
        """
        execute_query(_connection, insert_deposit_query, (transaction_id,customer_id, amount))

        print(f"Deposit of ${amount:.2f} successful for customer ID {customer_id}.")
    
    except Exception as e:
        print(f"Error during deposit: {e}")

def withdrawal(_connection, customer_id, password, amount):
    # Step 1: Authenticate the customer
    if not authentication_check(_connection, customer_id, password):
        print("Invalid credentials. Unable to perform withdrawal.")
        return
    
    # Step 2: Check if the customer has sufficient balance
    check_balance_query = """
        SELECT balance
        FROM customer
        WHERE customer_id = %s;
    """
    cursor = _connection.cursor()
    cursor.execute(check_balance_query, (customer_id,))

    current_balance = cursor.fetchall()[0][0]

    if current_balance < amount:
        print("Insufficient balance. Unable to perform withdrawal.")
        return

    try:
        # Step 3: Update customer balance
        update_balance_query = """
            UPDATE customer
            SET balance = balance - %s
            WHERE customer_id = %s;
        """
        execute_query(_connection, update_balance_query, (amount, customer_id))

        #record the transaction
        insert_transaction_query = """
            insert into transaction () values ();
        """
        cursor = _connection.cursor()
        cursor.execute(insert_transaction_query)

        transaction_id_query = "SELECT LAST_INSERT_ID() AS transaction_id;"
        cursor.execute(transaction_id_query)

        transaction_id = cursor.fetchall()[0][0]

        # Step 4: Record the withdrawal
        insert_widthdrawal_query = """
            INSERT INTO withdrawal 
                (transaction_id ,customer_id, amount) 
            VALUES (%s, %s, %s);
        """
        execute_query(_connection, insert_widthdrawal_query, (transaction_id,customer_id, amount))

        print(f"Withdrawal of ${amount:.2f} successful for customer ID {customer_id}.")
    
    except Exception as e:
        print(f"Error during withdrawal: {e}")

def transfer(_connection, source_customer_id, source_password, destination_customer_id, amount):
    # Step 1: Authenticate the source customer
    if not authentication_check(_connection, source_customer_id, source_password):
        print("Invalid credentials for source customer. Unable to perform transfer.")
        return
    
    # Step 2: Check if the customer has sufficient balance
    check_balance_query = """
        SELECT balance
        FROM customer
        WHERE customer_id = %s;
    """
    cursor = _connection.cursor()
    cursor.execute(check_balance_query, (source_customer_id,))

    current_balance = cursor.fetchall()[0][0]

    if current_balance < amount:
        print("Insufficient balance. Unable to perform withdrawal.")
        return

    try:
        # Step 3: Update source customer balance (debit)
        update_source_balance_query = """
            UPDATE customer
            SET balance = balance - %s
            WHERE customer_id = %s;
        """
        execute_query(_connection, update_source_balance_query, (amount, source_customer_id))

        # Step 4: Update destination customer balance (credit)
        update_destination_balance_query = """
            UPDATE customer
            SET balance = balance + %s
            WHERE customer_id = %s;
        """
        execute_query(_connection, update_destination_balance_query, (amount, destination_customer_id))

        #record the transaction
        insert_transaction_query = """
            insert into transaction () values ();
        """
        cursor = _connection.cursor()
        cursor.execute(insert_transaction_query)

        transaction_id_query = "SELECT LAST_INSERT_ID() AS transaction_id;"
        cursor.execute(transaction_id_query)

        transaction_id = cursor.fetchall()[0][0]

        # Step 5: Record the transfer
        insert_transfer_query = """
            INSERT INTO transfer 
                (transaction_id,from_account, to_account, amount) 
                VALUES (%s, %s, %s, %s);
        """
        execute_query(_connection, insert_transfer_query, (transaction_id,source_customer_id, destination_customer_id, amount))

        print(f"Transfer of ${amount:.2f} from customer ID {source_customer_id} to {destination_customer_id} successful.")
    
    except Exception as e:
        print(f"Error during transfer: {e}")

def show_transaction(_connection, customer_id, password):
    if not authentication_check(_connection, customer_id, password):
        print("Invalid credentials for source customer. Unable to perform transfer.")
        return
    
    deposit_query = """
        SELECT d.transaction_id as 'transaction_id', d.amount, 'Deposit' AS transaction_type, t.transaction_date
        FROM deposit d
        JOIN transaction t ON d.transaction_id = t.transaction_id
        WHERE d.customer_id = %s;
    """

    withdrawal_query = """
        SELECT d.transaction_id as 'transaction_id', d.amount, 'Withdrawal' AS transaction_type, t.transaction_date
        FROM withdrawal d
        JOIN transaction t ON d.transaction_id = t.transaction_id
        WHERE d.customer_id = %s;
    """

    transfer_query = """
        SELECT d.transaction_id as 'transaction_id', d.amount, 'Transfer' AS transaction_type, t.transaction_date
        FROM transfer d
        JOIN transaction t ON d.transaction_id = t.transaction_id
        WHERE d.from_account = %s;
    """

    credit_query = """
        SELECT d.transaction_id as 'transaction_id', d.amount, 'Credit' AS transaction_type, t.transaction_date
        FROM transfer d
        JOIN transaction t ON d.transaction_id = t.transaction_id
        WHERE d.to_account = %s;
    """


    cursor = _connection.cursor()

    cursor.execute(deposit_query, (customer_id,))
    deposit_result = cursor.fetchall()

    cursor.execute(withdrawal_query, (customer_id,))
    withdrawal_result = cursor.fetchall()

    cursor.execute(transfer_query, (customer_id,))
    transfer_result = cursor.fetchall()

    cursor.execute(credit_query, (customer_id,))
    credit_result = cursor.fetchall()

    # checking balance
    check_balance_query = """
        SELECT balance
        FROM customer
        WHERE customer_id = %s;
    """
    cursor = _connection.cursor()
    cursor.execute(check_balance_query, (customer_id,))

    current_balance = cursor.fetchall()[0][0]

    # Merge and sort the results from all queries
    all_results = deposit_result+ withdrawal_result + transfer_result + credit_result
    all_results = sorted(all_results, key=lambda x: x[0])

    if not all_results:
        print("No transactions found for the specified customer.")
        return
    
    print("\n\nTransaction History:")
    print("{:<20} {:<15} {:<20} {:<15}".format("Transaction ID", "Amount", "Transaction Type", "Transaction Date"))
    print("=" * 80)

    for row in all_results:
        transaction_id = row[0]
        amount = row[1]
        transaction_type = row[2]
        transaction_date = row[3]

        formatted_date = transaction_date.strftime("%Y-%m-%d %H:%M:%S")  # Adjust the format as needed

        print("{:<20} {:<15.2f} {:<20} {:<15}".format(transaction_id, amount, transaction_type, formatted_date))

    print("\nAvailable Balance : ", current_balance,"\n")

def create_sample_data(_connection):
    i = 0
    for new_account_data in sample_data.sample_customer_data:
        i += 1
        data = (
            new_account_data["first_name"],
            new_account_data["last_name"],
            new_account_data["email"],
            new_account_data["phone_number"],
            new_account_data["address"]
        )
        create_new_account(_connection, data, sample_data.sample_user_authentication_data[str(i)])
    
    for deposit_data in sample_data.sample_deposit_data:
        deposit(_connection, deposit_data["customer_id"], sample_data.sample_user_authentication_data[str(deposit_data["customer_id"])], deposit_data["amount"])

    for withdrawal_data in sample_data.sample_withdrawal_data:
        withdrawal(_connection, withdrawal_data["customer_id"], sample_data.sample_user_authentication_data[str(withdrawal_data["customer_id"])], withdrawal_data["amount"])

    for transfer_data in sample_data.sample_transfer_data:
        transfer(_connection, transfer_data["from_account"], sample_data.sample_user_authentication_data[str(transfer_data["from_account"])], transfer_data["to_account"], deposit_data["amount"])

    print("sample data added succesfully")
