import mysql.connector

def execute_query(connection, query, data=None):
    """Execute a query on the MySQL database."""
    try:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(host, user, password, database_name):
    # Connect to MySQL server
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

    # Create a cursor object
    cursor = connection.cursor()

    try:
        # Create the database
        cursor.execute(f"CREATE DATABASE {database_name}")
        print(f"Database '{database_name}' created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

def create_tables(host, user, password, database_name):
    _connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database_name
    )
    # Create the 'customer' table
    create_customer_table_query = """
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone_number VARCHAR(10),
            address VARCHAR(255),
            balance DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
    """
    execute_query(_connection, create_customer_table_query)

    # Create the 'user_authentication' table
    create_user_authentication_table_query = """
        CREATE TABLE IF NOT EXISTS user_authentication (
            customer_id INT PRIMARY KEY,
            password VARCHAR(255) NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
        );
    """
    execute_query(_connection, create_user_authentication_table_query)

    # Create the 'transaction' table
    create_transaction_table_query = """
        CREATE TABLE IF NOT EXISTS transaction (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    execute_query(_connection, create_transaction_table_query)

    # Create the 'withdrawal' table with a foreign key referencing 'transaction' table
    create_withdrawal_table_query = """
        CREATE TABLE IF NOT EXISTS withdrawal (
            transaction_id INT primary key,
            customer_id INT,
            amount DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES transaction(transaction_id),
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
        );
    """
    execute_query(_connection, create_withdrawal_table_query)

    # Create the 'deposit' table with a foreign key referencing 'transaction' table
    create_deposit_table_query = """
        CREATE TABLE IF NOT EXISTS deposit (
            transaction_id INT primary key,
            customer_id INT,
            amount DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES transaction(transaction_id),
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
        );
    """
    execute_query(_connection, create_deposit_table_query)

    # Create the 'transfer' table with foreign keys referencing 'transaction' and 'customer' tables
    create_transfer_table_query = """
        CREATE TABLE IF NOT EXISTS transfer (
            transaction_id INT primary key,
            from_account INT,
            to_account INT,
            amount DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES transaction(transaction_id),
            FOREIGN KEY (from_account) REFERENCES customer(customer_id),
            FOREIGN KEY (to_account) REFERENCES customer(customer_id)
        );
    """
    execute_query(_connection, create_transfer_table_query)

host = "localhost"
user = "root"
password = "123456"
database_name = "Bank_Management"

create_database(host, user, password, database_name)
create_tables(host, user, password, database_name)