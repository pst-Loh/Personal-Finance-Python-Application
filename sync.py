from datetime import datetime
import json
from requests_oauthlib import OAuth2Session
import pandas as pd
import sqlite3
import webbrowser
import base_calc

########### Task 1 ###########

# read the credentials from CSV-file "settings.csv"
settings = pd.read_csv("settings.csv")

# credentials
client_id = settings.iloc[0,1]
client_secret = settings.iloc[1,1]
token_url = settings.iloc[2,1]
authorization_url = settings.iloc[3,1]
redirect_url = settings.iloc[4,1]

# OAuth2.0 authentication
splitwise = OAuth2Session(client_id, redirect_uri= redirect_url)
authorization, state = splitwise.authorization_url(authorization_url)

# webbrowser module is used to start the webbrowser from within Python
webbrowser.open(authorization, new = 1) # opens the url in a new tab in the webbrowser

# log into Splitwise
# after that you can authorize the access and you will be redirected to:
# "https://dev.splitwise.com/?code=...&state=...#introduction" -> this URL has to be pasted in the input below
redirect_response = input("After redirection, please paste the full redirect URL here:" )

# getting the access token
splitwise.fetch_token(token_url=token_url, client_secret=client_secret,
                      authorization_response=redirect_response, include_client_id= True)


# Start of the programme
def start():
    get_data()                      # retrievement of data from Splitwise API
    create_tables()                 # creation of database "[userID].sqlite" if not existent yet
    insert_data_main_tables()       # insertion of data in the main tables "Users, Groups, Categories, Subcategories" if
                                    # not existent yet
    refresh_groups()                # in particular used for deleting groups from database that are not existing anymore
                                    # in Splitwise
    refresh_insertion_expenses()    # insertion in "Transactions" and "TransactionItems" tables
    refresh_deletion_expenses()     # deletion from "Transactions" and "TransactionItems" tables
    base_calc.currency_conversion(user_id)

    interface_start = 0
    if interface_start == 0:
        personal_finance.main()           # activates the interface (only once after programme was started) -> thereafter,
        interface_start += 1        # the interface is called by the different functions
    # currency_conversion(user_id)
    # unrec_transact(owed_share, net_balance)
    # income_insertion(user_id)


user_id = None
def get_data():
    # User data
    global user_id  # making "userID" available in the whole file
    global user_name
    current_user = splitwise.get("https://www.splitwise.com/api/v3.0/get_current_user")
    response1 = json.loads(current_user.text)
    user_id = response1["user"]["id"]
    user_name = "{first_name} {last_name}".format(first_name = response1["user"]["first_name"],
                                                  last_name = response1["user"]["last_name"])

    # Group data
    global group_id
    global group_name
    groups = splitwise.get("https://www.splitwise.com/api/v3.0/get_groups")
    response2 = json.loads(groups.text)
    group_list =response2["groups"]
    group_id = []
    group_name = []
    for group in group_list:
        group_id.append(group["id"])
        group_name.append(group["name"])


    # Category data
    global category_id
    global category_name
    categories = splitwise.get("https://secure.splitwise.com/api/v3.0/get_categories")
    response3 = json.loads(categories.text)
    categories_list = response3["categories"]
    category_id = []
    category_name = []
    for category in categories_list:
        category_id.append(category["id"])
        category_name.append(category["name"])


    # Subcategory data
    global subcategory_id
    global subcategory_name
    subcategory_id = []
    subcategory_name = []
    for category in categories_list:
        subcategories_list = category["subcategories"]
        for subcategory in subcategories_list:
            subcategory_id.append(subcategory["id"])
            subcategory_name.append(subcategory["name"])


    # Transactions data
    global transaction_id; global date; global expense_group_id; global expense_subcategory_id;
    global description; global currency; global repeatInterval; global updated; global deleted
    expenses = splitwise.get("https://secure.splitwise.com/api/v3.0/get_expenses")
    response4 = json.loads(expenses.text)
    expenses_list = response4["expenses"]
    transaction_id = []
    date = []
    expense_group_id = []
    expense_subcategory_id = []
    description = []
    currency = []
    repeatInterval = []
    updated = []
    deleted = []
    for expense in expenses_list:
        transaction_id.append(expense["id"])

        old_date = expense["date"]
                        # used to determine the current data format;  used to define new date format
        new_date =datetime.strptime(old_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y")
        date.append(new_date)

        expense_group_id.append(expense["group_id"])

        expense_subcategory_id.append(expense["category"]["id"])

        description.append(expense["description"])

        currency.append(expense["currency_code"])

        repeatInterval.append(expense["repeat_interval"])

        old_update = expense["updated_at"]
        new_update = datetime.strptime(old_update, "%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y %H:%M:%S")
        updated.append(new_update)

        if expense["deleted_at"] != None:
            deleted.append(expense["id"])

    # TransactionItems data
    global created_by_user_id; global owed_share; global net_balance; global expenses_df;
    created_by_user_id = []    # stores the ID of the user who has created the given expense
    owed_share = []            # share of user in expense
    net_balance = []           # net_balance of user in expense (for Task 4)

    for expense in expenses_list:
        created_by_user_id.append(expense["created_by"]["id"])

        # if the user has not contributed to an expense, his share is not available
        # to check this, Python verifies for each iteration if ID of current user is existent in expense["users"]
        all_users_id = []
        for id in range(0, len(expense["users"])):
            all_users_id.append(expense["users"][id]["user_id"])

        if user_id in all_users_id: # check if current userID is existent in list that contains all users that
                                    # contributed to the expense of the current iteration
                                    # if current user contributed to the expense, only his share will be selected
            for user in expense["users"]:
                if user["user_id"] == user_id:
                    owed_share.append(user["owed_share"])
                    net_balance.append(user["net_balance"])

        # if current user did not contribute to the expense, a "None"-value will be assigned to his share
        else:
            owed_share.append("0.0")
            net_balance.append("0.0")

                                             # index Dataframe              # indexposition: 0
    expenses_df = pd.DataFrame({"transactionID":transaction_id,             # indexposition: 1
                                "date": date,                               # indexposition: 2
                                "groupID": expense_group_id,                # indexposition: 3
                                "subcategoryID": expense_subcategory_id,    # indexposition: 4
                                "description": description,                 # indexposition: 5
                                "currency": currency,                       # indexposition: 6
                                "repeatInterval": repeatInterval,           # indexposition: 7
                                "updated": updated,                         # indexposition: 8
                                "userID": created_by_user_id,               # indexposition: 9
                                "amount": owed_share})                      # indexposition: 10
    # Insert new expenses
        # Currency codes
    global currency_code_list; global repeatInterval_dict; global possible_changes
    currencies = splitwise.get("https://secure.splitwise.com/api/v3.0/get_currencies")
    response5 = json.loads(currencies.text)
    currencies_available = response5["currencies"]
    currency_code_list = []
    for code in currencies_available:
        currency_code_list.append(code["currency_code"])

        # values for repeatInterval
    repeatInterval_dict = {"1": "never", "2": "weekly", "3": "fortnightly", "4": "monthly", "5": "yearly"}

    # Modify existing expense
        # data that can be changed
    possible_changes = {"1": "date", "2": "subcategoryID", "3": "description", "4": "currency",
                        "5": "repeatInterval", "6": "total expense amount"}


# creation of tables
def create_tables():
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id = user_id))
    cursor = conn.cursor()
    # Users table
    cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                      userID integer PRIMARY KEY,
                      name text)""")

    # Groups table
    cursor.execute("""CREATE TABLE IF NOT EXISTS Groups (
                      groupID integer PRIMARY KEY,
                      'group' text)""")

    # Categories table
    cursor.execute("""CREATE TABLE IF NOT EXISTS Categories (
                      categoryID integer PRIMARY KEY,
                      category text)""")

    # Subcategories table
    cursor.execute("""CREATE TABLE IF NOT EXISTS Subcategories (
                      subcategoryID integer PRIMARY KEY,
                      category text)""")

    # Transactions table
    cursor.execute("""CREATE TABLE IF NOT EXISTS Transactions (
                      transactionID integer PRIMARY KEY,
                      date text,
                      groupID integer,
                      subcategoryID integer,
                      description text,
                      currency text,
                      repeatInterval text,
                      updated text,
                      FOREIGN KEY (groupID) REFERENCES Groups(groupID),
                      FOREIGN KEY (subcategoryID) REFERENCES Subcategories(subcategoryID))""")

    # TransactionsItems table
    cursor.execute("""CREATE TABLE IF NOT EXISTS TransactionItems (
                      itemID integer PRIMARY KEY,
                      transactionID integer,
                      userID integer,
                      amount real,
                      baseAmount real,
                      FOREIGN KEY (transactionID) REFERENCES Transactions(transactionID),
                      FOREIGN KEY (userID) REFERENCES User(userID))""")
    conn.commit()
    conn.close()


def insert_data_main_tables():
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()
    cursor.execute("""INSERT OR IGNORE INTO Users VALUES (:userid, :name)""", {"userid": user_id,
                                                                               "name": user_name})

    for element in zip(group_id, group_name):
        cursor.execute("""INSERT OR IGNORE INTO Groups VALUES (:groupID, :group)""", {"groupID": element[0],
                                                                                      "group": element[1]})

    for element in zip(category_id, category_name):
        cursor.execute("""INSERT OR IGNORE INTO Categories VALUES (:categoryID, :category)""",
                                                                                     {"categoryID": element[0],
                                                                                      "category": element[1]})

    for element in zip(subcategory_id, subcategory_name):
        cursor.execute("""INSERT OR IGNORE INTO Subcategories VALUES (:subcategoryID, :category)""",
                                                                                    {"subcategoryID": element[0],
                                                                                     "category": element[1]})
    conn.commit()
    conn.close()


def refresh_groups():
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()
    # select all existing groups from database (except for income group)
    groups_database = cursor.execute("""SELECT groupID FROM Groups WHERE groupID != 10000000""").fetchall()
    groups_list = []
    for tuple in groups_database:
        groups_list.append(tuple[0])
    # compare existing groups from database with groups retrieved from Splitwise
    for id in groups_list:
        if id not in group_id: # delete group from database if it does not exist in Splitwise anymore
            cursor.execute("""DELETE FROM Groups WHERE groupID = {id}""".format(id = id))
    groups_list.clear() # reset of list
    conn.commit()
    conn.close()


# insertion in "Transactions" and "TransactionItems" tables
def refresh_insertion_expenses(): # refresh data in database -> only non-existing data should be added
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()
    # Transactions table
    for row in expenses_df.itertuples():  # each row is returned as a tuple
        # only add data of those expenses in table "Transactions" that are not existent yet and were not already deleted
        # if transactionID of an expense is not existent in "Transactions", it is added with all
        # the corresponding data
        if str(row[3]) == "nan": # if expense is not shared in Group (-> GroupID = nan), then the
                                 # expense has to be assigned to GroupID = 0 (= Non-expenses group)
            cursor.execute("""REPLACE INTO Transactions VALUES (:transactionID, :date, :groupID, 
                              :subcategoryID, :description, :currency, :repeatInterval, :updated)""",
                              {"transactionID": row[1], "date": row[2], "groupID": 0, "subcategoryID": row[4],
                              "description": row[5], "currency": row[6], "repeatInterval": row[7], "updated": row[8]})

        else:
            cursor.execute("""REPLACE INTO Transactions VALUES (:transactionID, :date, :groupID, 
                              :subcategoryID, :description, :currency, :repeatInterval, :updated)""",
                              {"transactionID": row[1], "date": row[2], "groupID": row[3], "subcategoryID": row[4],
                              "description": row[5], "currency": row[6], "repeatInterval": row[7], "updated": row[8]})


    # TransactionItems table
    items_in_transactionsitems = cursor.execute("""SELECT transactionID FROM TransactionItems""").fetchall()
    # since the SELECT statement returns a list of tuples it needs to be converted into list without tuples
    transaction_id_transactionitems_table = [] # list of transactionIDs from "TransactionItems" table
    for tuple in items_in_transactionsitems:
        for element in tuple:
            transaction_id_transactionitems_table.append(element)

    # generating our own itemID in "TransactionItems" table
    # the last itemID is selected to continue the counting process
    last_item_id = cursor.execute("""SELECT MAX(itemID) FROM TransactionItems""").fetchone()[0]
    if last_item_id == None:
        item_id = 1
    else:
        item_id = last_item_id + 1

    # insertion into "TransactionItems" table
    for row in expenses_df.sort_values("transactionID").itertuples():
        if row[1] not in transaction_id_transactionitems_table: # non-existing expenses will be inserted
            cursor.execute("""INSERT INTO TransactionItems (itemID, transactionID, userID, amount) 
                              VALUES (:itemID, :transactionID, :userID, :amount)""",
                              {"itemID": item_id, "transactionID": row[1], "userID": row[9], "amount": row[10]})
            item_id += 1

        elif row[1] in transaction_id_transactionitems_table: # existing expenses will be updated if data has changed
            existing_item_id = cursor.execute("""SELECT itemID FROM TransactionItems WHERE transactionID = {id}"""\
                                              .format(id = row[1])).fetchone()[0]
            cursor.execute("""REPLACE INTO TransactionItems (itemID, transactionID, userID, amount) 
                              VALUES (:itemID, :transactionID, :userID, :amount)""",
                              {"itemID": existing_item_id, "transactionID": row[1], "userID": row[9], "amount": row[10]})
    transaction_id_transactionitems_table.clear() # reset of list
    conn.commit()
    conn.close()


# deletion from "Transactions" and "TransactionItems" tables
def refresh_deletion_expenses():
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()
    for deleted_id in deleted:
        # select the current itemID of transaction that shall be deleted
        current_item_id = cursor.execute("""SELECT itemID FROM TransactionItems WHERE transactionID = {id}""" \
                                         .format(id = deleted_id)).fetchone()[0]

        # delete the transaction from "Transactions" and "TransactionItems" table
        cursor.execute("""DELETE FROM Transactions WHERE transactionID = {id}""".format(id = deleted_id))
        cursor.execute("""DELETE FROM TransactionItems WHERE transactionID = {id}""".format(id = deleted_id))

        # itemID of all subsequent transactions should be reduced by one
        cursor.execute("""UPDATE TransactionItems SET itemID = itemID - 1 WHERE itemID > {current_id}""" \
                          .format(current_id = current_item_id))
    conn.commit()
    conn.close()


# function to specify detailed shares when inserting new expense
def detailed_shares(cost, description, payment, selected_category, chosen_group_id, creation_method,
                    date_expense, currency_code, chosenInterval):
    option = 1
    group_info = splitwise.get("https://www.splitwise.com/api/v3.0/get_group/{group_id}"\
                               .format(group_id=chosen_group_id)) # get all information for the chosen GroupID
    response6 = json.loads(group_info.text)
    members = response6["group"]["members"]
    members_id_list = [dict["id"] for dict in members] # get the member's ID of the chosen group
    members_name_list = [dict["first_name"] + " " + dict["last_name"] for dict in members] # get the member's name
    print("\nBelow you can see the users with whom you can share the expense.")            # of the chosen group
    for member in zip(members_name_list, members_id_list): # print out the available users
        if member[1] != user_id:
            print("{option}) ID of {name}: {id}".format(option=option, name = member[0], id=member[1]))
            option += 1
    option = 1  # reset of variable to 1 (if new expense is created without stopping the programme)
    while True: # possibility to choose with how many users to share expense with
        try:
            number_users = int(input("\nWith how many users of the group do you want to share the expense? " + \
                             "Please enter the number here:"))
        except ValueError:
            print("Please enter numbers only (no decimals).")
        else:
            if number_users > len(members_id_list):
                print("You cannot share your expense with more than {numbers} users".format(numbers = len(number_users)))
            elif number_users < 1:
                print("You have to share your expense with at least one user.")
            else:
                break

    index = 1
    users_list = [] # list of entered userIDs (-> is needed to create dictionary (= value))
    users_index = [] # list of user designation (-> is needed to create dictionary (= key))
    while True: # enter the IDs of the users with whom to share expense with (logged in user is not considered)
        user_input1 = input("\nEnter the IDs of the users with whom you want to share the expense" +\
                           " (separated by commas):").split(",")
        try: # check if input can be converted into integer
            for id in user_input1:
                users_list.append(int(id))
                users_index.append("users__{index}__user_id".format(index = index))
                index +=1
        except ValueError:
            print("No decimals or symbols allowed.")
            users_list.clear()
            users_index.clear()
            index = 1
        else: # here, it is necessary to check if the number of users with whom expense should be shared corresponds
              # to the number of IDs that was entered
            if len(users_list) > number_users:
                print("You entered more users than you have indicated before. Try again.")
                users_list.clear()
                users_index.clear()
                index = 1
            elif len(users_list) < number_users:
                print("You entered less users than you have indicated before. Try again.")
                users_list.clear()
                users_index.clear()
                index = 1
            else: # also check if the userIDs are existing
                if all(id in members_id_list for id in users_list):
                    users_list.insert(0, user_id)
                    users_index.insert(0, "users__0__user_id")
                    index = 0 # reset of variable to 0 (for next block below)
                    break
                else:
                    print("Some ID(s) that you entered is/are not existing. Try again.")
                    users_list.clear()
                    users_index.clear()
                    index = 1

    print("\nNow you have to enter the amount of paid share. This basically means who has paid how much?")
    print("Please enter the amounts with two decimals and in the correct order (starting with your amount " +\
          "and then continuing with the order in which you entered the userIDs above).""")
    print("Please also note to enter '0.00' if a user did not pay anything.")
    users_paid_share = [] # list of entered paid shares (-> is needed to create dictionary (= value))
    paid_share_index = [] # list of paid share designation (-> is needed to create dictionary (= key))
    while True: # enter the paid shares of all users (including the logged in user)
        user_input2 = input("\nEnter the amounts here (including you) (separated by commas):").split(",")
        try: # check if input can be converted into float
            for share in user_input2:
                share = "{:.2f}".format(float(share))
                users_paid_share.append(float(share))
                paid_share_index.append("users__{index}__paid_share".format(index = index))
                index +=1
        except ValueError:
            print("Please enter numbers (using . as decimal separator).")
            users_paid_share.clear()
            paid_share_index.clear()
            index = 0
        else: # here, it is necessary to check if the number of shares corresponds to the number of userIDs
              # that were entered above
            if len(users_paid_share) > len(users_list):
                print("You can only enter {number} shares. Try again.".format(number = len(users_list)))
                users_paid_share.clear()
                paid_share_index.clear()
                index = 0
            elif len(users_paid_share) < len(users_list):
                print("You did not enter shares for all users. Try again.")
                users_paid_share.clear()
                paid_share_index.clear()
                index = 0
            else:
                if sum(users_paid_share) != float(cost):
                    print("The shares you have entered must be equal to total amount of expense ({amount})"\
                          .format(amount = cost))
                    users_paid_share.clear()
                    paid_share_index.clear()
                    index = 0
                else:
                    index = 0 # reset of variable to 0 (for next block below)
                    break

    print("\nNow you have to enter the amount of owed share. This basically means who should have paid how much?")
    print("Please enter the amounts with two decimals and in the correct order (starting with your amount " + \
          "and then continuing with the order in which you entered the userIDs above).""")
    print("Please also note to enter '0.00' if a user should not have paid anything.")
    users_owed_share = []  # list of entered owed shares (-> is needed to create dictionary (= value))
    owed_share_index = []  # list of owed share designation (-> is needed to create dictionary (= key))
    while True:  # enter the owed shares of all users (including the logged in user)
        user_input3 = input("\nEnter the amounts here (including you) (separated by commas):").split(",")
        try:  # check if input can be converted into float
            for share in user_input3:
                share = "{:.2f}".format(float(share))
                users_owed_share.append(float(share))
                owed_share_index.append("users__{index}__owed_share".format(index=index))
                index += 1
        except ValueError:
            print("Please enter numbers (using . as decimal separator).")
            users_owed_share.clear()
            owed_share_index.clear()
            index = 0
        else:  # here, it is necessary to check if the number of shares corresponds to the number of userIDs
            # that were entered above
            if len(users_owed_share) > len(users_list):
                print("You can only enter {number} shares. Try again.".format(number=len(users_list)))
                users_owed_share.clear()
                owed_share_index.clear()
                index = 0
            elif len(users_owed_share) < len(users_list):
                print("You did not enter shares for all users. Try again.")
                users_owed_share.clear()
                owed_share_index.clear()
                index = 0
            else:
                if sum(users_owed_share) != float(cost):
                    print("The shares you have entered must be equal to total amount of expense ({amount})" \
                          .format(amount=cost))
                    users_owed_share.clear()
                    owed_share_index.clear()
                    index = 0
                else:
                    index = 1 # reset of variable to 1 (if new expense is created without stopping the programme)
                    break

    additional_values_dict = {"cost": cost, "description": description, "payment": payment,
                              "category_id": selected_category,"group_id": chosen_group_id,
                              "creation_method": creation_method, "date": date_expense, "currency_code": currency_code,
                              "repeat_Interval": chosenInterval}
    user_index_dict = {user[0] : user[1] for user in zip(users_index, users_list)}
    user_paid_share_dict = {user[0] : str(user[1]) for user in zip(paid_share_index, users_paid_share)}
    user_owed_share_dict = {user[0]: str(user[1]) for user in zip(owed_share_index, users_owed_share)}

    # reset the lists of this function for new iteration
    members_id_list.clear(); members_name_list.clear(); users_list.clear(); users_index.clear();
    users_paid_share.clear(); paid_share_index.clear(); users_owed_share.clear(); owed_share_index.clear()
    while True:  # asks user if he really wants to insert new expense
        check1 = input("Do you really want to insert this expense? (Y/N):")
        if check1 == "Y":
            # merging the four dicts from above to one single dict
            new_expense = {**additional_values_dict, **user_index_dict, **user_paid_share_dict, **user_owed_share_dict}
            splitwise.post("https://secure.splitwise.com/api/v3.0/create_expense", data=new_expense)
            # reset the dictionaries of this function for new iteration
            additional_values_dict.clear(); user_index_dict.clear(); user_paid_share_dict.clear();
            user_owed_share_dict.clear(); new_expense.clear()
            return start()  # after insertion of expense, programme will be run again to insert new expense
                             # into database -> therefore, no expense will be forgotten
        elif check1 == "N":
            # reset the dictionaries of this function for new iteration
            additional_values_dict.clear(); user_index_dict.clear(); user_paid_share_dict.clear();
            user_owed_share_dict.clear();

            return personal_finance.main()
        else:
            print("Just enter Y or N (capital letters).")


def insert_new_expenses(selected_category):
    # amount of expense
    while True:  # user has to enter a valid amount for the expense
        try:
            cost_input = float(input("\nPlease enter the total amount of the expense:"))
        except ValueError:
            print("Please enter numbers only.")
        else:
            break

    cost = "{:.2f}".format(cost_input)  # the amount is converted to float with 2 decimals
    while True:  # asks user if the amount is correct (necessary, since if user enters float with 3 decimals,
                 # the amount is rounded to 2 decimals and maybe it is not the expense that user wanted to enter)
        check2 = input("Is {} the amount that you want to insert? (Y/N):".format(cost))
        if check2 == "Y":
            break
        elif check2 == "N":
            return insert_new_expenses(selected_category)
        else:
            print("Just enter Y or N (capital letters).")

    # description of expense
    description = input("\nEnter a short description of your expense (e.g. 'Rent', 'Cinema'):")
    print()

    # payment
    payment = "false"  # it is assumed that user only enters expenses, no payments to another person

    # groupID for expense
    option = 1
    for tuple in zip(group_name, group_id):
        print("{option}) ID of {groupname}:  {groupid}".format(option = option, groupname = tuple[0],
                                                               groupid = tuple[1]))
        option += 1
    option = 1  # reset of variable to 1 (for new expense without stopping the programme)
    while True: # user has to input an existing GroupID
        try:
            group_input = int(input("For which group do you want to enter the expense? Enter groupID:"))
        except ValueError:
            print("Please enter numbers only (no decimals).")
        else:
            if group_input not in group_id:
                print("This groupID does not exist. Please try again.")
            else:
                break
    chosen_group_id = group_input

    # date of expense
    while True:
        try: # # user can enter date in the specified format; no letters should be entered, therefore int-input
            date_input = int(input("\nPlease enter the date of the expense. " + \
                                   "Herefore, please enter the date in the following format (yyyymmdd):"))
        except ValueError:
            print("Please enter numbers only (no decimals).")
        else:
            if (len(str(date_input)) < 8) or (len(str(date_input)) > 8):
                print("You have to enter exactly 8 characters.")
            elif (str(date_input)[4:6] < "01") or (str(date_input)[4:6] > "12"):
                print("Month must be value between 01 and 12.")
            elif (str(date_input)[6:] < "01") or (str(date_input)[6:] > "31"):
                print("Day must be value between 01 and 31.")
            else:
                break
    date_expense = date_input + 1 # increase date by 1, because Splitwise takes date - 1

    # currency of expense
    while True:
        currency_input = input("\nPlease enter the currency code (in capital letters):")
        if any(character.isdigit() for character in currency_input):
            print("No numbers needed here. Please enter a valid currency code.")
        elif currency_input not in currency_code_list:
            print("This currency code does not exist. Try again.")
        else:
            break
    currency_code = currency_input

    # repeatInterval of expense
    print("\nHow often does your expense repeat?")
    for i in repeatInterval_dict:
        print(i + ")", repeatInterval_dict[i])
    while True:
        repeatInterval_input = input("Please choose an option:")
        if repeatInterval_input in repeatInterval_dict:
            break
        else:
            print("This option does not exist. Please try again.")
    chosenInterval = repeatInterval_dict["{input}".format(input = repeatInterval_input)]

    # sharing of expense (only possible if not GroupID = 0 was chosen)
    if chosen_group_id != 0:
        while True:
            split_input = input("\nDo you want to split the expense equally? (Y/N):")
            if split_input == "Y":
                split_equally = "true"
                creation_method = "equal" # indicates that expense is split equally
                break
            elif split_input == "N":
                creation_method = "unequal"
                detailed_shares(cost, description, payment, selected_category, chosen_group_id, creation_method,
                                date_expense, currency_code, chosenInterval) # call function detailed_shares
            else:
                print("Just enter Y or N (capital letters).")

        while True:  # asks user if he really wants to insert new expense
            check3 = input("Do you really want to insert this expense? (Y/N):")
            if check3 == "Y":
                new_expense = {"cost": cost, "description": description, "payment": payment,
                               "category_id": selected_category, "group_id": chosen_group_id,
                               "split_equally": split_equally, "creation_method": creation_method,
                               "date": date_expense, "currency_code": currency_code,
                               "repeat_interval": chosenInterval}
                splitwise.post("https://secure.splitwise.com/api/v3.0/create_expense", data=new_expense)
                # reset the dictionary of this function for new iteration
                new_expense.clear()
                return start() # after insertion of expense, programme will be run again to insert new expense
                               # into database -> therefore, no expense will be forgotten
            elif check3 == "N":
                return personal_finance.main()
            else:
                print("Just enter Y or N (capital letters).")
    # if GroupID = 0, the expense cannot be shared with other users, since only member of this group is user
    # who is currently logged into Splitwise
    else:
        while True:  # asks user if he really wants to insert new expense
            check4 = input("Do you really want to insert this expense? (Y/N):")
            if check4 == "Y":
                new_expense = {"cost": cost, "description": description, "payment": payment,
                               "category_id": selected_category, "group_id": chosen_group_id,
                               "split_equally" : "true", "creation_method": "equal",
                               "date": date_expense, "currency_code": currency_code, "repeat_interval": chosenInterval}
                splitwise.post("https://secure.splitwise.com/api/v3.0/create_expense", data=new_expense)
                # reset the dictionary of this function for new iteration
                new_expense.clear()
                return start()  # after insertion of expense, programme will be run again to insert new expense
                                # into database -> therefore, no expense will be forgotten
            elif check4 == "N":
                return personal_finance.main()
            else:
                print("Just enter Y or N (capital letters).")


# modification of an existing expense
def modify_existing_expense(selected_category):
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()
    option = 1
    print("\nFor which of the following groups do you want to modify an expense?")
    for tuple in zip(group_name, group_id):
        print("{option}) ID of {groupname}:  {groupid}".format(option=option, groupname=tuple[0],
                                                               groupid=tuple[1]))
        option += 1
    option = 1  # reset of variable to 1 (for new expense without stopping the programme)
    while True:  # user has to input an existing GroupID
        try:
            group_input = int(input("Please enter a groupID:"))
        except ValueError:
            print("Please enter numbers only (no decimals).")
        else:
            if group_input not in group_id:
                print("This groupID does not exist. Please try again.")
            else:
                break

    # select data for all expenses that are corresponding to the selected category and the selected group
    selected_transactions = cursor.execute("""SELECT T.description, T.transactionID, TI.amount 
                                              FROM Transactions AS T \
                                              INNER JOIN TransactionItems AS TI
                                                ON TI.transactionID = T.transactionID
                                              WHERE T.subcategoryID = {category_id} 
                                              AND T.groupID = {group_id}""" \
                                           .format(category_id=selected_category, group_id = group_input)).fetchall()
    selection_dict = {}
    if not selected_transactions:  # if no expenses are existing yet, return to interface
        print("No expenses exist yet for the selected category and group. First you need to create a new expense.")
        personal_finance.main()

    print("\nWhich of the following transactions do you want to modify?")
    for expense in selected_transactions: # display all expenses that are corresponding to the selected category
        selection_dict.update({"{option}".format(option=option): expense[1]})  # dictionary ={"option": transactionID}
        print("{option}) {description}, ID: {id}, Amount: {amount}".format(option=option, description=expense[0],
                                                                           id=expense[1], amount=expense[2]))
        option += 1
    while True:
        try: # user can choose an expense that he want to modify
            user_input = int(input("Please choose an option to modify:"))
        except ValueError:
            print("Please enter numbers only (no decimals).")
        else:
            if (user_input > len(selected_transactions)) or (user_input < 1):
                print("This option is not available! Please try again.")
            else:
                chosen_transaction = selection_dict[str(user_input)]
                selection_dict.clear() # reset the dictionary of this function for new iteration
                break

    print("\nDo you really want to modify the expense with ID {id}?".format(id = chosen_transaction))
    while True:
        check5 = input("Please enter Y or N:")
        if check5 == "Y": # retrieve all data regarding the chosen expense from Splitwise API
            option = 1   # reset of variable to 1 (for new expense without stopping the programme)
            break
        elif check5 == "N":
            option = 1   # reset of variable to 1 (for new expense without stopping the programme)
            return personal_finance.main()
        else:
            print("Just enter Y or N (capital letters).")

    print("\nWhat do you want to change?")
    for i in possible_changes: # display the options the user has to modify an expense
        print(i + ")", possible_changes[i])
    while True:
        change_input = input("Please choose an option:")
        if change_input in possible_changes:
            break
        else:
            print("This option does not exist. Please try again.")
    chosen_change = possible_changes["{input}".format(input = change_input)]
    if chosen_change == "date":
        modification_date(chosen_transaction, selected_category)           # call function to modify date of expense
    elif chosen_change == "subcategoryID":
        modification_subcategoryID(chosen_transaction, selected_category)  # call function to modify subcategory of expense
    elif chosen_change == "description":
        modification_description(chosen_transaction, selected_category)    # call function to modify description of expense
    elif chosen_change == "currency":
        modification_currency(chosen_transaction, selected_category)       # call function to modify currency of expense
    elif chosen_change == "repeatInterval":
        modification_repeatInterval(chosen_transaction, selected_category) # call function to modify repeatInterval of expense
    elif chosen_change == "total expense amount":
        modification_amount(chosen_transaction, selected_category)          # call function to modify total amount of expense
    conn.commit()
    conn.close()


# modification of date of expense
def modification_date(chosen_transaction, selected_category):
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()

    while True:
        try: # user can enter new date in the specified format; no letters should be entered, therefore int-input
            new_date_input = int(input("\nPlease enter the new date of the expense. " + \
                                       "Herefore, please enter the date in the following format (yyyymmdd):"))
        except ValueError:
            print("Please enter numbers only (no decimals).")
        else:
            if (len(str(new_date_input)) < 8) or (len(str(new_date_input)) > 8):
                print("You have to enter exactly 8 characters.")
            elif (str(new_date_input)[4:6] < "01") or (str(new_date_input)[4:6] > "12"):
                print("Month must be value between 01 and 12.")
            elif (str(new_date_input)[6:] < "01") or (str(new_date_input)[6:] > "31"):
                print("Day must be value between 01 and 31.")
            else: # new date will be inserted in database and in Splitwise for chosen expense
                date_convertion = datetime.strptime(str(new_date_input), "%Y%m%d").strftime("%d.%m.%Y")
                cursor.execute("""UPDATE Transactions SET date = '{new_date}' WHERE transactionID = {chosen_id}""" \
                                  .format(new_date = date_convertion, chosen_id = chosen_transaction))

                update_expense = {"date": new_date_input + 1} # increase date by 1, because Splitwise takes date - 1
                splitwise.post("https://secure.splitwise.com/api/v3.0/update_expense/{id}" \
                               .format(id=chosen_transaction), data=update_expense)
                conn.commit()
                conn.close()
                break
    while True:
        check6 = input("\nDo you want to modify another data? (Y/N):")
        if check6 == "Y":
            return modify_existing_expense(selected_category)
        elif check6 == "N":
            return personal_finance.main()
        else:
            print("Just enter Y or N (capital letters).")


# modification of subcategoryID of expense
def modification_subcategoryID(chosen_transaction, selected_category):
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()
    option = 1                                    # index Dataframe     # indexposition: 0
    subcategory_df =  pd.DataFrame({"subcategory": subcategory_name,    # indexposition: 1
                                    "subcategoryID": subcategory_id,})  # indexposition: 2
    print("\nThese are the subcategories you can choose between:")
    for row in subcategory_df.sort_values("subcategoryID").itertuples():
        print("{option}) Subcategory: {subcategory}, ID: {id}".format(option=option, subcategory=row[1],
                                                                        id=row[2]))
        option += 1
    option = 1  # reset of variable to 1 (for new expense without stopping the programme)
    while True:
        try: # user can enter new subcategory for expense
            new_category_input = int(input("Please enter the new subcategoryID:"))
        except ValueError:
            print("Please enter numbers only (no decimals).")
        else:
            if new_category_input not in subcategory_id:
                print("This subcategory does not exist. Please try again.")
            else: # new subcategory will be inserted in database and in Splitwise for chosen expense
                cursor.execute("""UPDATE Transactions SET subcategoryID = {new_id} WHERE transactionID = {chosen_id}""" \
                               .format(new_id=new_category_input, chosen_id=chosen_transaction))

                update_expense = {"category_id": new_category_input}
                splitwise.post("https://secure.splitwise.com/api/v3.0/update_expense/{id}" \
                               .format(id=chosen_transaction), data=update_expense)
                conn.commit()
                conn.close()
                break
    while True:
        check7 = input("\nDo you want to modify another data? (Y/N):")
        if check7 == "Y":
            return modify_existing_expense(selected_category)
        elif check7 == "N":
            return personal_finance.main()
        else:
            print("Just enter Y or N (capital letters).")


# modification of description of expense
def modification_description(chosen_transaction, selected_category):
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()
    new_description_input = input("\nPlease enter a short new description of the expense (e.g. 'Rent', 'Cinema'):")
    # new description will be inserted in database and in Splitwise for chosen expense
    cursor.execute("""UPDATE Transactions SET description = '{new_description}' WHERE transactionID = {chosen_id}""" \
                   .format(new_description=new_description_input, chosen_id=chosen_transaction))

    update_expense = {"description": new_description_input}
    splitwise.post("https://secure.splitwise.com/api/v3.0/update_expense/{id}" \
                   .format(id=chosen_transaction), data=update_expense)
    conn.commit()
    conn.close()
    while True:
        check8 = input("\nDo you want to modify another data? (Y/N):")
        if check8 == "Y":
            return modify_existing_expense(selected_category)
        elif check8 == "N":
            return personal_finance.main()
        else:
            print("Just enter Y or N (capital letters).")


# modification of currency of expense
def modification_currency(chosen_transaction, selected_category):
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()
    while True:
        new_currency_input = input("\nPlease enter the new currency code (in capital letters):")
        if any(character.isdigit() for character in new_currency_input):
            print("No numbers needed here. Please enter a valid currency code.")
        elif new_currency_input not in currency_code_list:
            print("This currency code does not exist. Try again.")
        else:   # new currency will be inserted in database and in Splitwise for chosen expense
            cursor.execute("""UPDATE Transactions SET currency = '{new_currency}' WHERE transactionID = {chosen_id}""" \
                           .format(new_currency=new_currency_input, chosen_id=chosen_transaction))

            update_expense = {"currency_code": new_currency_input}
            splitwise.post("https://secure.splitwise.com/api/v3.0/update_expense/{id}" \
                           .format(id=chosen_transaction), data=update_expense)
            conn.commit()
            conn.close()
            break
    while True:
        check9 = input("\nDo you want to modify another data? (Y/N):")
        if check9 == "Y":
            return modify_existing_expense(selected_category)
        elif check9 == "N":
            return personal_finance.main()
        else:
            print("Just enter Y or N (capital letters).")


# modification of repeatInterval of expense
def modification_repeatInterval(chosen_transaction, selected_category):
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()
    print("\nHow often does your expense repeat?")
    for i in repeatInterval_dict:
        print(i + ")", repeatInterval_dict[i])
    while True:
        new_repeatInterval_input = input("Please choose a new interval by selecting an option:")
        if new_repeatInterval_input in repeatInterval_dict:
            break
        else:
            print("This option does not exist. Please try again.")
    new_chosenInterval = repeatInterval_dict["{input}".format(input = new_repeatInterval_input)]
    cursor.execute("""UPDATE Transactions SET repeatInterval = '{new_interval}' WHERE transactionID = {chosen_id}""" \
                   .format(new_interval=new_chosenInterval, chosen_id=chosen_transaction))

    update_expense = {"repeat_interval": new_chosenInterval}
    splitwise.post("https://secure.splitwise.com/api/v3.0/update_expense/{id}" \
                   .format(id=chosen_transaction), data=update_expense)
    conn.commit()
    conn.close()
    while True:
        check10 = input("\nDo you want to modify another data? (Y/N):")
        if check10 == "Y":
            return modify_existing_expense(selected_category)
        elif check10 == "N":
            return personal_finance.main()
        else:
            print("Just enter Y or N (capital letters).")


# modification of amount of expense
def modification_amount(chosen_transaction, selected_category):
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()
    # get data about the chosen transaction
    chosen_expense = splitwise.get("https://secure.splitwise.com/api/v3.0/get_expense/{id}" \
                                    .format(id = chosen_transaction))
    response7 = json.loads(chosen_expense.text)
    expense_data = response7["expense"]
    splitting = expense_data["creation_method"] # is expense split equally or unequally
    current_amount = expense_data["cost"] + " " + expense_data["currency_code"]
    user_involved = expense_data["users"] # all users who are involved in expense

    print("\nThe current total amount of expense is {current_amount}.".format(current_amount=current_amount))
    print("Please be aware that if you want to change the currency, you have to select option 2).")
    while True:  # user has to enter a valid amount for the expense
        try:
            new_cost_input = float(input("\nPlease enter the new total amount of the expense:"))
        except ValueError:
            print("Please enter numbers only.")
        else:
            break

    cost = "{:.2f}".format(new_cost_input)  # the amount is converted to float with 2 decimals
    while True:  # asks user if the amount is correct (necessary, since if user enters float with 3 decimals,
                 # the amount is rounded to 2 decimals and maybe it is not the expense that user wanted to enter)
        check2 = input("Is {} the amount that you want to insert? (Y/N):".format(cost))
        if check2 == "Y":
            break
        elif check2 == "N":
            return modification_amount(chosen_transaction,selected_category)
        else:
            print("Just enter Y or N (capital letters).")

    if splitting == "equal":
        index = 0
        # user_id
        # dictionary = {"users__{index}__user_id": paid share}
        user_index_dict = {}
        for user in user_involved:
            user_index_dict.update({"users__{index}__user_id".format(index = index): user["user_id"]})
            index += 1

        # user_paid_share
        print("\nYou have to enter the new amounts of paid share for every user involved (Who has paid how much?)")
        print("Please enter the amounts with two decimals in the the following order:")
        for user in user_involved:
            print("- {user_first_name} {user_last_name} (ID: {user_id})" \
                  .format(user_first_name = user["user"]["first_name"], user_last_name = user["user"]["last_name"],
                          user_id = user["user_id"]))
        print("Please also note to enter '0.00' if a user did not pay anything.")

        index = 0  # reset of variable to 0 (for block below)
        new_users_paid_share = []  # list of entered paid shares (-> is needed to create dictionary (= value))
        paid_share_index = []      # list of paid share designation (-> is needed to create dictionary (= key))
        while True:  # enter the paid shares of all users (including the logged in user)
            user_input = input("\nEnter the amounts in correct order here (separated by commas):").split(",")
            try:  # check if input can be converted into float
                for share in user_input:
                    share = "{:.2f}".format(float(share))
                    new_users_paid_share.append(float(share))
                    paid_share_index.append("users__{index}__paid_share".format(index=index))
                    index += 1
            except ValueError:
                print("Please enter numbers (using . as decimal separator).")
                new_users_paid_share.clear()
                paid_share_index.clear()
                index = 0
            else:  # here, it is necessary to check if the number of shares corresponds to the number of users
                    # involved in expense
                if len(new_users_paid_share) > len(user_involved) :
                    print("You can only enter {number} shares. Try again.".format(number=len(user_involved)))
                    new_users_paid_share.clear()
                    paid_share_index.clear()
                    index = 0
                elif len(new_users_paid_share) < len(user_involved):
                    print("You did not enter shares for all users. Try again.")
                    new_users_paid_share.clear()
                    paid_share_index.clear()
                    index = 0
                else:
                    if sum(new_users_paid_share) != float(cost):
                        print("The shares you have entered must be equal to total amount of expense ({amount})" \
                              .format(amount=cost))
                        new_users_paid_share.clear()
                        paid_share_index.clear()
                        index = 0
                    else:
                        index = 0  # reset of variable to 0
                        break

        # user_owed_share
        print("\nNo need to enter new amounts for the owed shares of the users since expense is split euqally.")
        # dictionary = {"users__{index}__owed_share": paid share}
        user_owed_share_dict = {}
        for index in range(0, len(user_involved)):
            user_owed_share_dict.update({"users__{index}__owed_share".format(index=index): rounded_user_share})

        # dictionary = {"users__{index}__paid_share": paid share}
        user_paid_share_dict = {user[0]: str(user[1]) for user in zip(paid_share_index, new_users_paid_share)}

        # dictionary contains all the values that have changed
        update_expense = { "cost": cost, **user_index_dict, **user_paid_share_dict, **user_owed_share_dict}
        splitwise.post("https://secure.splitwise.com/api/v3.0/update_expense/{id}" \
                        .format(id=chosen_transaction), data=update_expense)

        # if expense is split equally then amount in TransactionItems must be adjusted accordingly
        new_user_share = float(cost) / len(user_involved)
        rounded_user_share = "{:.2f}".format(new_user_share)
        cursor.execute("""UPDATE TransactionItems SET amount = {new_amount} WHERE transactionID = {chosen_id}""" \
                       .format(new_amount=float(rounded_user_share), chosen_id=chosen_transaction))
        conn.commit()
        conn.close()

    if splitting == "unequal":
        index = 0
        # user_id
        # dictionary = {"users__{index}__user_id": paid share}
        user_index_dict = {}
        for user in user_involved:
            user_index_dict.update({"users__{index}__user_id".format(index=index): user["user_id"]})
            index += 1

        # user_paid_share
        print("\nYou have to enter the new amounts of paid share for every user involved (Who has paid how much?)")
        print("Please enter the amounts with two decimals in the the following order:")
        for user in user_involved:
            print("- {user_first_name} {user_last_name} (ID: {user_id})" \
                  .format(user_first_name=user["user"]["first_name"], user_last_name=user["user"]["last_name"],
                          user_id=user["user_id"]))
        print("Please also note to enter '0.00' if a user did not pay anything.")

        index = 0  # reset of variable to 0 (for block below)
        new_users_paid_share = []  # list of entered paid shares (-> is needed to create dictionary (= value))
        paid_share_index = []  # list of paid share designation (-> is needed to create dictionary (= key))
        while True:  # enter the paid shares of all users (including the logged in user)
            user_input = input("\nEnter the amounts in correct order here (separated by commas):").split(",")
            try:  # check if input can be converted into float
                for share in user_input:
                    share = "{:.2f}".format(float(share))
                    new_users_paid_share.append(float(share))
                    paid_share_index.append("users__{index}__paid_share".format(index=index))
                    index += 1
            except ValueError:
                print("Please enter numbers (using . as decimal separator).")
                new_users_paid_share.clear()
                paid_share_index.clear()
                index = 0
            else:  # here, it is necessary to check if the number of shares corresponds to the number of users
                # involved in expense
                if len(new_users_paid_share) > len(user_involved):
                    print("You can only enter {number} shares. Try again.".format(number=len(user_involved)))
                    new_users_paid_share.clear()
                    paid_share_index.clear()
                    index = 0
                elif len(new_users_paid_share) < len(user_involved):
                    print("You did not enter shares for all users. Try again.")
                    new_users_paid_share.clear()
                    paid_share_index.clear()
                    index = 0
                else:
                    if sum(new_users_paid_share) != float(cost):
                        print("The shares you have entered must be equal to total amount of expense ({amount})" \
                              .format(amount=cost))
                        new_users_paid_share.clear()
                        paid_share_index.clear()
                        index = 0
                    else:
                        index = 0  # reset of variable to 0
                        break

        # user_owed_share
        print("\nYou have to enter the new amounts of owed share for every user involved (Who should have paid how much?)")
        print("Please enter the amounts with two decimals in the the following order:")
        for user in user_involved:
            print("- {user_first_name} {user_last_name} (ID: {user_id})" \
                  .format(user_first_name=user["user"]["first_name"], user_last_name=user["user"]["last_name"],
                          user_id=user["user_id"]))
        print("Please also note to enter '0.00' if a user should not have paid anything.")

        index = 0  # reset of variable to 0 (for block below)
        new_users_owed_share = []  # list of entered owed shares (-> is needed to create dictionary (= value))
        owed_share_index = []      # list of owed share designation (-> is needed to create dictionary (= key))
        while True:  # enter the owed shares of all users (including the logged in user)
            user_input1 = input("\nEnter the amounts in correct order here (separated by commas):").split(",")
            try:  # check if input can be converted into float
                for share in user_input1:
                    share = "{:.2f}".format(float(share))
                    new_users_owed_share.append(float(share))
                    owed_share_index.append("users__{index}__owed_share".format(index=index))
                    index += 1
            except ValueError:
                print("Please enter numbers (using . as decimal separator).")
                new_users_owed_share.clear()
                owed_share_index.clear()
                index = 0
            else:  # here, it is necessary to check if the number of shares corresponds to the number of userIDs
                # that were entered above
                if len(new_users_owed_share) > len(user_involved):
                    print("You can only enter {number} shares. Try again.".format(number=len(user_involved)))
                    new_users_owed_share.clear()
                    owed_share_index.clear()
                    index = 0
                elif len(new_users_owed_share) < len(user_involved):
                    print("You did not enter shares for all users. Try again.")
                    new_users_owed_share.clear()
                    owed_share_index.clear()
                    index = 0
                else:
                    if sum(new_users_owed_share) != float(cost):
                        print("The shares you have entered must be equal to total amount of expense ({amount})" \
                              .format(amount=cost))
                        new_users_owed_share.clear()
                        owed_share_index.clear()
                        index = 0
                    else:
                        index = 0  # reset of variable to 0
                        break

        # dictionary = {"users__{index}__owed_share": owed share}
        user_owed_share_dict = {user[0]: str(user[1]) for user in zip(owed_share_index, new_users_owed_share)}

        # dictionary = {"users__{index}__paid_share": paid share}
        user_paid_share_dict = {user[0]: str(user[1]) for user in zip(paid_share_index, new_users_paid_share)}

        # dictionary contains all the values that have changed
        update_expense = {"cost": cost, **user_index_dict, **user_paid_share_dict, **user_owed_share_dict}
        splitwise.post("https://secure.splitwise.com/api/v3.0/update_expense/{id}" \
                       .format(id=chosen_transaction), data=update_expense)

        # searching for the owed share of user who is currently logged in to insert it as new amount in "TransactionItems"
        for key1 in user_index_dict:
            if user_index_dict[key1] == user_id: # userID in dict must be equal to userID of user who is logged in
                for key2 in user_owed_share_dict:
                    if key1[0:8] in key2:   # looking for the key, that corresponds to user who is logged in
                        new_user_share = float(user_owed_share_dict[key2])    # select the owed share of the corresponding key

        cursor.execute("""UPDATE TransactionItems SET amount = {new_amount} WHERE transactionID = {chosen_id}""" \
                       .format(new_amount=new_user_share, chosen_id=chosen_transaction))
        conn.commit()
        conn.close()

    while True:
        check11 = input("\nDo you want to modify another data? (Y/N):")
        if check11 == "Y":
            return modify_existing_expense(selected_category)
        elif check11 == "N":
            return personal_finance.main()
        else:
            print("Just enter Y or N (capital letters).")

# deletion of existing expense
def delete_existing_expense(selected_category):
    conn = sqlite3.connect("{user_id}.sqlite".format(user_id=user_id))
    cursor = conn.cursor()
    option = 1
    print("\nFor which of the following groups do you want to modify an expense?")
    for tuple in zip(group_name, group_id):
        print("{option}) ID of {groupname}:  {groupid}".format(option=option, groupname=tuple[0],
                                                               groupid=tuple[1]))
        option += 1
    option = 1  # reset of variable to 1 (for new expense without stopping the programme)
    while True:  # user has to input an existing GroupID
        try:
            group_input = int(input("Please enter a groupID:"))
        except ValueError:
            print("Please enter numbers only (no decimals).")
        else:
            if group_input not in group_id:
                print("This groupID does not exist. Please try again.")
            else:
                break

    # select data for all expenses that are corresponding to the selected category and the selected group
    selected_transactions = cursor.execute("""SELECT T.description, T.transactionID, TI.amount 
                                              FROM Transactions AS T \
                                              INNER JOIN TransactionItems AS TI
                                                ON TI.transactionID = T.transactionID
                                              WHERE T.subcategoryID = {id} 
                                              AND T.groupID = {group_id}"""\
                                              .format(id = selected_category, group_id=group_input)).fetchall()
    selection_dict = {}
    if not selected_transactions: # if no expenses are existing yet, return to interface
        print("No expenses exist yet for the selected category and group. First you need to create a new expense.")
        personal_finance.main()

    # if only one expense is existing for chosen category, directly ask user if expense shall be deleted
    elif len(selected_transactions) == 1:
        print("\nDo you want to delete the following transaction from Splitwise and the database?" + \
              "\n 1) {description}, ID: {id}, Amount: {amount}".format(description=selected_transactions[0][0],
                                                                       id=selected_transactions[0][1],
                                                                       amount=selected_transactions[0][2]))
        while True:
            user_input = input("Please enter Y or N:")
            if user_input == "Y":
                splitwise.post("https://secure.splitwise.com/api/v3.0/delete_expense/{id}"\
                               .format(id = selected_transactions[0][1]))

                # select the current itemID of transaction that shall be deleted
                current_item_id = cursor.execute("""SELECT itemID FROM TransactionItems WHERE transactionID = {id}""" \
                                                 .format(id=selected_transactions[0][1])).fetchone()[0]

                # delete the transaction from "Transactions" and "TransactionItems" table
                cursor.execute("""DELETE FROM Transactions WHERE transactionID = {id}""" \
                               .format(id = selected_transactions[0][1]))
                cursor.execute("""DELETE FROM TransactionItems WHERE transactionID = {id}""" \
                               .format(id = selected_transactions[0][1]))

                # itemID of all subsequent transactions should be reduced by one
                cursor.execute("""UPDATE TransactionItems SET itemID = itemID - 1 WHERE itemID > {current_id}""" \
                               .format(current_id=current_item_id))
                conn.commit()
                conn.close()
                start()
            elif user_input == "N":
                return personal_finance.main()
            else:
                print("Just enter Y or N (capital letters).")

    # if more than one expense is existing for chosen category, ask user which expense he would like to deleted
    else:
        print("\nWhich of the following transactions do you want to delete from Splitwise and the database?")
        for expense in selected_transactions: # display all expenses that are corresponding to the selected category
            selection_dict.update({"{option}".format(option = option): expense[1]}) # dictionary ={"option": transactionID}
            print("{option}) {description}, ID: {id}, Amount: {amount}".format(option = option, description = expense[0],
                                                                               id = expense[1], amount = expense[2]))
            option += 1
        while True:
            try:
                user_input = int(input("Please enter the number of the expense you want to delete:"))
            except ValueError:
                print("Please enter numbers only (no decimals).")
            else:
                if (user_input > len(selected_transactions)) or (user_input < 1):
                    print("This option is not available! Please try again.")
                else:
                    break

        print("\nDo you really want to delete the expense with ID {id}?".format(id = selection_dict[str(user_input)]))
        while True:
            check12 = input("Please enter Y or N:")
            if check12 == "Y":
                splitwise.post("https://secure.splitwise.com/api/v3.0/delete_expense/{id}"\
                              .format(id = selection_dict[str(user_input)]))

                # select the current itemID of transaction that shall be deleted
                current_item_id = cursor.execute("""SELECT itemID FROM TransactionItems WHERE transactionID = {id}""" \
                                                 .format(id=selection_dict[str(user_input)])).fetchone()[0]

                # delete the transaction from "Transactions" and "TransactionItems" table
                cursor.execute("""DELETE FROM Transactions WHERE transactionID = {id}""" \
                               .format(id = selection_dict[str(user_input)]))
                cursor.execute("""DELETE FROM TransactionItems WHERE transactionID = {id}""" \
                               .format(id = selection_dict[str(user_input)]))

                # itemID of all subsequent transactions should be reduced by one
                cursor.execute("""UPDATE TransactionItems SET itemID = itemID - 1 WHERE itemID > {current_id}""" \
                               .format(current_id=current_item_id))

                selection_dict.clear() # reset the dictionary of this function for new iteration
                option = 1             # reset of variable to 1 (for new expense without stopping the programme)
                conn.commit()
                conn.close()
                start()
            elif check12 == "N":
                option = 1             # reset of variable to 1 (for new expense without stopping the programme)
                return personal_finance.main()
            else:
                print("Just enter Y or N (capital letters).")

import personal_finance # Task 7
start() # launches the programme