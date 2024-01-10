import Database_functions
import UI

if __name__ == "__main__" :
    connection = Database_functions.connect_to_database("localhost", "root", "123456", "Bank_Management") # create a database before running this code

    # Database_functions.create_sample_data(connection) # imports sample data

    while True :
        UI.display_main_menu()
        choice = UI.get_user_choice()

        if choice == '1':
            data = UI.create_account()
            Database_functions.create_new_account(connection, *data)
        
        elif choice == '2':
            data = UI.deposit()
            Database_functions.deposit(connection, *data)

        elif choice == '3':
            data = UI.widthdrawal()
            Database_functions.withdrawal(connection, *data)

        elif choice == '4':
            data = UI.transfer()
            Database_functions.transfer(connection, *data)

        elif choice == '5':
            data = UI.view_transaction()
            Database_functions.show_transaction(connection, *data)

        else :
            break
    
    Database_functions.close_connection(connection)
