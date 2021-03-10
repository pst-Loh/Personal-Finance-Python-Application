import sqlite3
from datetime import datetime


def income_insertion(user_id):  #main algorithm starts here

    with sqlite3.connect("{user_id}.sqlite".format(user_id=user_id)) as conn:
        cursor = conn.cursor()

    # to insert Categories table with INCOME type
    #this func can be run multiple times but can ignore itself if repeated
    def insert_Categories():
        cursor.execute("""INSERT or IGNORE INTO Categories (categoryID, category) VALUES ('100', 'Income')""")
        conn.commit()

    insert_Categories()

    # to insert Subcategories table with sub-income types
    #this func can be run multiple times but can ignore itself if repeated
    def insert_Subcategories():
        cursor.execute("""INSERT or IGNORE INTO Subcategories (subcategoryID, category) VALUES 
            ('101', 'Income Salary'),
            ('102', 'Income Business'),
            ('103', 'Income Gifts'),
            ('104', 'Income Grants'),
            ('105', 'Income Other')
            """)
        conn.commit()

    insert_Subcategories()


    #define a dictionary for income categoryies
    income_dict = {'101': 'Income Salary', '102': 'Income Business', '103': 'Income Gifts', '104': 'Income Grants',
                   '105': 'Income Other'}
    print('Income options:', income_dict)


    # ask user to input income (sub)category
    def income_category():
        while True:
            input_category = input('Choose category by enter 101,102,103,104 or 105: ')
            if input_category in income_dict:
                return income_dict[input_category]
            else:
                print('Invalid input, please enter again')

    cat = income_category()  #return subcategory type in dict


    def get_key(val):
        for key, value in income_dict.items():
            if val == value:
                return key

    catID = get_key(cat)     #return subcategory ID number in dict

    # ask user to input income amt
    def income_amount():
        while True:
            try:
                income_amt = float(input('Enter income amount in EUR: '))
                return income_amt
            except ValueError:
                print('Invalid input, please enter valid number')

    amt = income_amount()    #return income amount

    # ask user to input income date
    def income_date():
        while True:
            try:
                income_date = datetime.strptime(input('Enter Start date in the format d.m.y:'), '%d.%m.%Y').strftime(
                    "%d.%m.%Y")
                return income_date
            except ValueError:
                print("Invalid input, please enter correct format")

    dat = income_date()      #return income date

    # ask user to input income interval
    def income_interval():
        interval_list = ['weekly', 'fortnightly', 'monthly', 'never']
        while True:
            income_interval = str(input('Choose if it is weekly, fortnightly, monthly or never: '))
            if income_interval in interval_list:
                return income_interval
            else:
                print("Invalid input, please enter correct interval")
    inc_interval = income_interval()      #return income interval


    last_item_id = cursor.execute("""SELECT MAX(itemID) FROM TransactionItems""").fetchone()[0]
    item_id = last_item_id + 1
    transactionID_income = item_id  #we take transactionsID for income data is the same as itemID


    #TransactionItems table insertion
    cursor.execute("""INSERT OR IGNORE INTO TransactionItems (itemID, transactionID, userID, amount) 
                            VALUES (:itemID, :transactionID, :userID, :amount)""",
                   {'itemID': item_id, 'transactionID': transactionID_income, 'userID': user_id, 'amount': amt})

    date_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    # Transactions table insertion
    cursor.execute("""INSERT OR IGNORE INTO Transactions VALUES (:transactionID, :date, :groupID, 
        :subcategoryID, :description, :currency, :repeatInterval, :updated)""",
                   {"transactionID": transactionID_income, "date": dat, "groupID": '10000000' , "subcategoryID": catID ,
                    "description": cat, "currency": 'EUR', 'repeatInterval': inc_interval, "updated": date_time})

    conn.commit()
    print('Income data added to database, return to User Interface')


#income_insertion(33463455)