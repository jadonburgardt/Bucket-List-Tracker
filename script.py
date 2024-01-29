# imports to save user data
import json
import atexit

# https://www.youtube.com/watch?v=T7s3st6xfpA
# https://opensource.com/article/19/7/save-and-load-data-python-json

# Function to save data with JSON
def save_data(accounts, bucket_lists, completed_items):
    # Open 'data.json' 
    with open('data.json', 'w') as file:
        # Create a dictionary to hold user data
        data = {
            "accounts": accounts,           # User account info
            "bucket_lists": bucket_lists,   # User bucket lists organized by categories and items
            "completed_items": completed_items  # User completed items organized by categories
        }

        # Write the data dictionary into the 'data.json' file in JSON format
        json.dump(data, file)

# Function to load saved data with JSON
def load_data():
    try:
        # opens file in read mode ('r')
        with open('data.json', 'r') as file:
            data = json.load(file)

            # grab user account information from the loaded data
            loaded_accounts = data.get("accounts", {})
            # grab user bucket lists from the loaded data
            loaded_bucket_lists = data.get("bucket_lists", {})
            # grab user completed items from the loaded data
            loaded_completed_items = data.get("completed_items", {})

            # Update the categories list
            global categories
            categories = list(set(category for user_lists in loaded_bucket_lists.values() for category in user_lists.keys()))

            # Returns the account information, bucket lists, and completed items
            return loaded_accounts, loaded_bucket_lists, loaded_completed_items
    except FileNotFoundError:
        return {}, {}, {}

# Login Function
def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

 # Check if the entered username exists in the accounts dictionary and the password matches
    if username in accounts and accounts[username] == password:
        print("Login successful!")
        manage_list(username)
        return True
    else:
        print("Invalid Information! Please try again.")
        return False

# Create Account Function
def create_account():
    new_username = input("Enter your new username: ")
    # Check if the entered username already exists in accounts dict
    if new_username in accounts:
        print("Username already exists! Please enter a different username.")

        # Return False if unsuccesful
        return False
    else:
        # Prompt the user to enter a new password for the account
        new_password = input("Enter your new password: ")

        # Add the new username and password to the accounts dictionary
        accounts[new_username] = new_password

        # create an empty bucket list for the new user
        bucket_lists[new_username] = {}

        # create an empty completed items list for the new user
        completed_items[new_username] = {}

        # Reset the global categories list to an empty list
        global categories
        categories = []

        # Print a success message for the account creation
        print("Account created successfully!")

        # Return True to if account is succesfully created
        return True

# Manage list area once logged in
def manage_list(username):
    print(f"Welcome {username}!")
    print("(1) to view bucket list categories")
    print("(2) to view completed bucket list items")
    print("(3) to logout")

    option = int(input("Enter your choice: "))

    if option == 1:
        view_categories(username)
    elif option == 2:
        print("View completed items goes here.")
        view_completed_items(username)
    elif option == 3:
        print("Goodbye!")
    else:
        print("Invalid choice! Please try again.")

# If 1 is entered from manage_list, to view bucket list categories
def view_categories(username):
    print("Bucket List Categories:")
    # Numbers each category
    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    category_option = int(input("\nEnter the number of the category to view, (0) to go back, (-1) to add a new category, (-2) to delete a category, or (-3) to logout: "))

    if category_option == 0:
        manage_list(username)
    elif category_option == -1:
        add_category(username)
    elif category_option == -2:
        delete_category(username)
    elif category_option == -3:
        print("Goodbye!")
    elif 0 <= category_option <= len(categories):
        if category_option == -2:  
            view_completed_items(username)
        else:
            view_lists(username, categories[category_option - 1])
    else:
        print("Invalid choice! Please try again.")

## view the completed items function
def view_completed_items(username):
    if username in completed_items:
        print("Completed Bucket List Items:")
        for category, items_info in completed_items[username].items():
            print(f"\nCategory: {category}")
            for item_info in items_info:
                print(f"Item: {item_info['item']}")
                print(f"Note: {item_info['note']}")
                print(f"Completion Date: {item_info['completion_date']}\n")

        print("\nOptions:")
        print("(0) Go back to main menu")
        print("(-1) Logout")
        print("(-2) Delete a completed item")

        option = int(input("Enter your choice: "))
        if option == 0:
            manage_list(username)
        elif option == -1:
            print("Logging out. Goodbye!")
        elif option == -2:
            delete_completed_item(username)
        else:
            print("Invalid choice. Please try again.")
            view_completed_items(username)
    else:
        print("No completed items to display.")
        manage_list(username)

# function to delete completed item from completed items
def delete_completed_item(username):
    item_name = input("Enter the name of the completed item you want to delete: ")

    # run through categories and items in the completed_items dictionary for user
    for category, items_info in completed_items.get(username, {}).items():
        # Iterate through each item_info dictionary in the list and number each one
        for index, item_info in enumerate(items_info):
            # Check if the 'item' key in the item_info dictionary matches the item_name
            if item_info['item'] == item_name:
                # Remove the completed item from the list in the current category
                deleted_item = completed_items[username][category].pop(index)
                print(f"Completed Item '{deleted_item['item']}' deleted from Category '{category}'.")

                # If the category becomes empty after deleting the item, remove the entire category
                if not completed_items[username][category]:
                    del completed_items[username][category]

                # If there are no more categories for the user, remove the username entry
                if not completed_items[username]:
                    del completed_items[username]

                # Call the function to view the updated list of completed items
                view_completed_items(username)

                # Exit the function after the item is deleted
                return

    # If no completed item with the specified name is found, print an error message
    print(f"No completed item with the name '{item_name}' found.")
    
    # Call the function to view the current list of completed items
    view_completed_items(username)

# Add category inside of view_categories
def add_category(username):
    new_category = input("Enter the name of the new category: ")

    # check if new category is not already in
    if new_category not in categories:
        # if not, add to global list
        categories.append(new_category)

    # checks the same for the list items inside the dictionaries
    if username not in bucket_lists:
        bucket_lists[username] = {}

    # Check if the new category is not already in the user's categories
    if new_category not in bucket_lists[username]:
        # If not, create an entry for the new category as an empty list in the user's dictionary
        bucket_lists[username][new_category] = []

    print(f"New category '{new_category}' added.")

    # Redirect the user to view the items within the new category
    view_lists(username, new_category)

# delete category within view_categories
# Function to delete a category from the user's bucket list
def delete_category(username):
    # Print the available categories for the user to choose from
    print("Available Categories to Delete:")
    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    category_option = int(input("Enter the number of the category to delete, (0) to go back, or (-1) to logout: "))

    # Check if the entered option is within the range of categories
    if 1 <= category_option <= len(categories):
        # Get the name of the category
        category_name = categories[category_option - 1]

        # Prompt the user to confirm the deletion
        confirm_delete = input(f"Are you sure you want to delete the category '{category_name}'? (yes/no): ")

        # Check the users confirmation
        if confirm_delete.lower() == "yes":
            # Remove the category from the global list of categories
            categories.remove(category_name)

            # Check if the user has an entry in the bucket_lists dictionary
            if username in bucket_lists and category_name in bucket_lists[username]:
                # Delete the category from the bucket list
                del bucket_lists[username][category_name]

            print(f"Category '{category_name}' deleted.")

            # Redirect the user to view the updated list
            view_categories(username)
        else:
            # If the user doest confirm, go back to viewing categories
            view_categories(username)
    elif category_option == 0:
        # If the user enters 0, go back to viewing categories
        view_categories(username)
    elif category_option == -1:
        print("Logging out. Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        delete_category(username)


# Delete a list item from a category
def delete_item_from_category(username, category):
    # Check if the user has a bucket list and if the category exists
    if username in bucket_lists and category in bucket_lists[username]:
        print(f"Items in Category '{category}':")
        for index, item in enumerate(bucket_lists[username][category], start=1):
            print(f"{index}. {item}")

        index_to_delete = int(input("Enter the number of the item to delete (0 to cancel): "))

        # Check if the entered index is within the valid range of items
        if 1 <= index_to_delete <= len(bucket_lists[username][category]):
            # Pop the deleted item 
            deleted_item = bucket_lists[username][category].pop(index_to_delete - 1)
            print(f"Item '{deleted_item}' deleted from Category '{category}'.")
        elif index_to_delete != 0:
            print("Invalid item number. No item deleted.")
    else:
        print("No items to delete.")


# Function to add an item to the category
def add_item_to_category(username, category):
    new_item = input("Enter the name of the new item: ")

    # Check if the user has a bucket list, if not create an empty bucket list
    if username not in bucket_lists:
        bucket_lists[username] = {}

    # Check if the category exists in the user bucket list, if not create the category
    if category not in bucket_lists[username]:
        bucket_lists[username][category] = []

    # Append the new item to bucket list
    bucket_lists[username][category].append(new_item)

    print(f"New item '{new_item}' added to Category '{category}'.")

    # After adding the item, view the updated list for the category
    view_lists(username, category)

# function to view list in specific categories
def view_lists(username, category):
    print(f"Category '{category}':")

    # Check if the user and the category exist in bucket lists
    if username in bucket_lists and category in bucket_lists[username]:
        # Get the list of items in the specific category
        items = bucket_lists[username][category]

        # Check if there are no items in the category
        if not items:
            # Prompt the user to add an item if the category is empty
            add_item_prompt = input("There are no items currently in this list! Do you want to enter an item? (yes/no): ")
            
            # If the user wants to add an item, call the add_item_to_category function
            if add_item_prompt.lower() == "yes":
                add_item_to_category(username, category)
            else:
                # If the user chooses not to add an item, tell them and go back to category view
                print("No items in this category.")
                view_categories(username)

        else:
            exit_loop = False

            while not exit_loop:
                for index, item in enumerate(items, start=1):
                    print(f"{index}. {item}")

                option = int(input("Enter (1) to complete item, (2) to delete item, "
                                   "(3) to add item, (0) to go back, or (-1) to logout: "))

                if option == 0:
                    exit_loop = True
                    view_categories(username)
                elif option == -1:
                    print("Logging out. Goodbye!")
                    exit_loop = True
                elif option == 2:
                    delete_item_from_category(username, category)
                elif option == 3:
                    add_item_to_category(username, category)
                elif option == 1:
                    complete_item(username, category)
                else:
                    print("Invalid choice. Please try again.")

    else:
        # If the user or the category doesn't exist, tell the user and go back to category view
        print("No items in this category.")
        add_item_prompt = input("There are no items currently in this list! Do you want to enter an item? (yes/no): ")
        if add_item_prompt.lower() == "yes":
            add_item_to_category(username, category)
        else:
            # If the user chooses not to add an item, tell them and go back to category view
            print("No items added.")
            view_categories(username)
            
# Function to complete an item in the category list
def complete_item(username, category):
    # Display the items in the specified category
    print(f"Items in Category '{category}':")
    items = bucket_lists[username][category]

    for index, item in enumerate(items, start=1):
        print(f"{index}. {item}")

    index_to_complete = int(input("Enter the number of the item to mark as completed (0 to cancel): "))

    if 1 <= index_to_complete <= len(items):
        # If a item index is chosen, mark the item as completed
        completed_item = items.pop(index_to_complete - 1)

        note = input("Add a note about your experience: ")

        completion_date = input("Enter the date you completed the item (YYYY-MM-DD): ")

        # Call the function to store the completed item info
        store_completed_item(username, category, completed_item, note, completion_date)

        print(f"Item '{completed_item}' marked as completed in Category '{category}'.")
    elif index_to_complete != 0:
        print("Invalid item number. No item marked as completed.")


# store complete item so that viewer can actually view their information 
def store_completed_item(username, category, completed_item, note, completion_date):
    # Check if the username exists in the completed_items dictionary
    if username not in completed_items:
        completed_items[username] = {}
    
    # Check if the category exists in the completed items for the unique user
    if category not in completed_items[username]:
        completed_items[username][category] = []

    # Append information about the completed item to the completed items dict
    completed_items[username][category].append({
        "item": completed_item,
        "note": note,
        "completion_date": completion_date
    })


# dictionary to store bucket lists inside categories
bucket_lists = {}

# list of categories holding items
categories = []

#dictionary to save completed items
completed_items = {}

# handles the choices made in list_option, ex. 0 to go back, -1 to logout...
def handle_list_option(list_option, username):
    if list_option == 1:
        add_item_to_category(username)
    elif list_option == 2:
        delete_item_from_category(username)
    elif list_option == 3:
        print("Going back to the main menu.")
    elif list_option == 4:
        print("Logging out. Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        list_option = int(input("Enter (1) to add item, enter (2) to delete an item, enter (3) to go back, "
                                "enter (4) to logout: "))

# way to load and register saved data from account 
accounts, bucket_lists, completed_items = load_data()
atexit.register(save_data, accounts, bucket_lists, completed_items)

# start program function
def start_program():
    logged_in = False

    while not logged_in:
        start = int(input("Welcome to your bucket list tracker!\nEnter (1) to login or enter (2) to create an account.\n"))

        if start == 1:
            logged_in = login()
        elif start == 2:
            create_account()
            print("Please login with your new information.")
        else:
            print("Unacceptable Input, Please try again.")

start_program()