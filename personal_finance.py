import sync
import sys
import Income
import Report
import unrec_transact


# input validity
class NonPlausibleInput(Exception):
    def __init__(self, value):
        self.value = value

# initializing expenses
class Expense:
    def __init__(self, amount, categoryId, date):
        self.amount = amount
        self.categoryId = categoryId
        self.date = date

# user input procedure
def main():
    running = False
    while running == False:
        running2 = False
        Inquiry = input('What do you want to do?'
                        '\n1 - Expenses'
                        '\n2 - Income'
                        '\n3 - Financial Report'
                        '\n4 - Financial Prediction'
                        '\n5 - Exit'
                        '\n')

        ######## Expenses

        if Inquiry == '1':
            while running2 == False:
                running3 = False
                try:
                    Category = int(input('\n--------------------\n'
                                         '\nExpenses\n'
                                         '\n0 - Go back'
                                         '\n1 - Entertainment'
                                         '\n2 - Food and drink'
                                         '\n3 - Home'
                                         '\n4 - Life'
                                         '\n5 - Transportation'
                                         '\n6 - Uncategorized'
                                         '\n7 - Utilities'

                                         '\nTo which category belongs this expense. Choose the number: '))

                    if Category < 0:
                        raise NonPlausibleInput(Category)
                    elif Category > 7:
                        raise NonPlausibleInput(Category)

                    ################### Category - Entertainment

                    elif Category == 1:
                        while running3 == False:
                            running4 = False
                            try:
                                Subcategory = int(input('\n--------------------\n'
                                                        '\nEntertainment\n'
                                                        '\n0 - Go back'
                                                        '\n1 - Games'
                                                        '\n2 - Movies'
                                                        '\n3 - Music'
                                                        '\n4 - Other'
                                                        '\n5 - Sports'
                                                        '\n Choose subcategory: '))

                                if Subcategory < 0:
                                    raise NonPlausibleInput(Subcategory)
                                elif Subcategory > 5:
                                    raise NonPlausibleInput(Subcategory)

                                ############################### Entertainment - Subcategories

                                elif Subcategory == 1:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 20
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 20
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 20
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 2:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 21
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 21
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 21
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 3:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 22
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 22
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 22
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 4:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 23
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 23
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 23
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 5:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 24
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 24
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 24
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 0:
                                    running3 = True

                            # Subcategory
                            except ValueError:
                                print("\n-- Integers only --\n")
                            except NonPlausibleInput:
                                print("\n-- Selection only --\n")


                    #################### Category - Food and drink

                    elif Category == 2:

                        while running3 == False:
                            running4 = False
                            try:
                                Subcategory = int(input('\n--------------------\n'
                                                        '\nFood and drink\n'
                                                        '\n0 - Go back'
                                                        '\n1 - Dining out'
                                                        '\n2 - Groceries'
                                                        '\n3 - Liquor'
                                                        '\n4 - Other'
                                                        '\n Choose subcategory: '))

                                if Subcategory < 0:
                                    raise NonPlausibleInput(Subcategory)
                                elif Subcategory > 4:
                                    raise NonPlausibleInput(Subcategory)

                                ############################### Food and drink - Subcategories

                                elif Subcategory == 1:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 13
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 13
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 13
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 2:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 12
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 12
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 12
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 3:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 38
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 38
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 38
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 4:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 26
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 26
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 26
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 0:
                                    running3 = True

                            # Subcategory
                            except ValueError:
                                print("\n-- Integers only --\n")
                            except NonPlausibleInput:
                                print("\n-- Selection only --\n")


                    #################### Category - Home

                    elif Category == 3:

                        while running3 == False:
                            running4 = False
                            try:
                                Subcategory = int(input('\n--------------------\n'
                                                        '\nHome\n'
                                                        '\n0 - Go back'
                                                        '\n1 - Electronics'
                                                        '\n2 - Furniture'
                                                        '\n3 - Household supplies'
                                                        '\n4 - Maintenance'
                                                        '\n5 - Mortgage'
                                                        '\n6 - Other'
                                                        '\n7 - Pets'
                                                        '\n8 - Rent'
                                                        '\n9 - Services'
                                                        '\n Choose subcategory: '))

                                if Subcategory < 0:
                                    raise NonPlausibleInput(Subcategory)
                                elif Subcategory > 9:
                                    raise NonPlausibleInput(Subcategory)

                                ############################### Home - Subcategories

                                elif Subcategory == 1:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 39
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 39
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 39
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 2:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 16
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 16
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 16
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 3:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 14
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 14
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 14
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 4:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 17
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 17
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 17
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 5:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 4
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 4
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 4
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 6:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 28
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 28
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 28
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 7:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 29
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 29
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 29
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 8:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 3
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 3
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 3
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 9:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 30
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 30
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 30
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 0:
                                    running3 = True

                            # Subcategory
                            except ValueError:
                                print("\n-- Integers only --\n")
                            except NonPlausibleInput:
                                print("\n-- Selection only --\n")


                    ################### Category - Life
                    elif Category == 4:
                        running2 = True

                        while running3 == False:
                            running4 = False
                            try:
                                Subcategory = int(input('\n--------------------\n'
                                                        '\nLife\n'
                                                        '\n0 - Go back'
                                                        '\n1 - Childcare'
                                                        '\n2 - Clothing'
                                                        '\n3 - Education'
                                                        '\n4 - Gifts'
                                                        '\n5 - Insurance'
                                                        '\n6 - Medical expenses'
                                                        '\n7 - Other'
                                                        '\n8 - Taxes'
                                                        '\n Choose subcategory: '))

                                if Subcategory < 0:
                                    raise NonPlausibleInput(Subcategory)
                                elif Subcategory > 8:
                                    raise NonPlausibleInput(Subcategory)

                                ############################### Life - Subcategories

                                elif Subcategory == 1:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 50
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 50
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 50
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 2:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 41
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 41
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 41
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 3:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 49
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 49
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 49
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 4:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 42
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 42
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 42
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 5:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 10
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 10
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 10
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 6:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 43
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 43
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 43
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 7:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 44
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 44
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 44
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 8:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 45
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 45
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 45
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 0:
                                    running3 = True

                            # Subcategory
                            except ValueError:
                                print("\n-- Integers only --\n")
                            except NonPlausibleInput:
                                print("\n-- Selection only --\n")


                    #################### Cateogry - Transportation
                    elif Category == 5:
                        running2 = True

                        while running3 == False:
                            running4 = False
                            try:
                                Subcategory = int(input('\n--------------------\n'
                                                        '\nTransportation\n'
                                                        '\n0 - Go back'
                                                        '\n1 - Bicycle'
                                                        '\n2 - Bus / train'
                                                        '\n3 - Car'
                                                        '\n4 - Gas / fuel'
                                                        '\n5 - Hotel'
                                                        '\n6 - Other'
                                                        '\n7 - Parking'
                                                        '\n8 - Plane'
                                                        '\n9 - Taxi'
                                                        '\n Choose subcategory: '))

                                if Subcategory < 0:
                                    raise NonPlausibleInput(Subcategory)
                                elif Subcategory > 9:
                                    raise NonPlausibleInput(Subcategory)

                                ############################### Transportation - Subcategories

                                elif Subcategory == 1:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 46
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 46
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 46
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 2:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 32
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 32
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 32
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 3:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 15
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 15
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 15
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 4:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 33
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 33
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 33
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 5:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 47
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 47
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 47
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 6:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 34
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 34
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 34
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 7:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 9
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 9
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 9
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 8:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 35
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 35
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 35
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 9:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 36
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 36
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 36
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 0:
                                    running3 = True

                            # Subcategory
                            except ValueError:
                                print("\n-- Integers only --\n")
                            except NonPlausibleInput:
                                print("\n-- Selection only --\n")



                    #################### Category - Uncategorized
                    elif Category == 6:
                        running2 = True

                        while running3 == False:
                            running4 = False
                            try:
                                Subcategory = int(input('\n--------------------\n'
                                                        '\nUncategorized\n'
                                                        '\n0 - Go back'
                                                        '\n1 - General'))

                                if Subcategory < 0:
                                    raise NonPlausibleInput(Subcategory)
                                elif Subcategory > 1:
                                    raise NonPlausibleInput(Subcategory)

                                ############################### Uncategorized - Subcategories

                                elif Subcategory == 1:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 18
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 18
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 18
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 0:
                                    running3 = True

                            # Subcategory
                            except ValueError:
                                print("\n-- Integers only --\n")
                            except NonPlausibleInput:
                                print("\n-- Selection only --\n")


                    #################### Category - Utilities
                    elif Category == 7:
                        running2 = True

                        while running3 == False:
                            running4 = False
                            try:
                                Subcategory = int(input('\n--------------------\n'
                                                        '\nUtilities\n'
                                                        '\n0 - Go back'
                                                        '\n1 - Cleaning'
                                                        '\n2 - Electricity'
                                                        '\n3 - Heat / gas'
                                                        '\n4 - Other'
                                                        '\n5 - Trash'
                                                        '\n6 - Tv / phone / internet'
                                                        '\n7 - Water'))

                                if Subcategory < 0:
                                    raise NonPlausibleInput(Subcategory)
                                elif Subcategory > 7:
                                    raise NonPlausibleInput(Subcategory)

                                ############################### Utilities - Subcategories

                                elif Subcategory == 1:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 48
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 48
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 48
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 2:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 5
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 5
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 5
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 3:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 6
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 6
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 6
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 4:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 11
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 11
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 11
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 5:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 37
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 37
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 37
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 6:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 8
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 8
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 8
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 7:
                                    while running4 == False:
                                        try:
                                            Action = int(input('\n--------------------\n'
                                                               '\nType of action\n'
                                                               '\n0 - Go back'
                                                               '\n1 - Add expense'
                                                               '\n2 - Modify expense'
                                                               '\n3 - Delete expense'
                                                               '\n Choose action: '))
                                            if Action < 0:
                                                raise NonPlausibleInput(Action)
                                            elif Action > 3:
                                                raise NonPlausibleInput(Action)
                                            elif Action == 1:
                                                selected_category = 7
                                                sync.insert_new_expenses(selected_category)
                                            elif Action == 2:
                                                selected_category = 7
                                                sync.modify_existing_expense(selected_category)
                                            elif Action == 3:
                                                selected_category = 7
                                                sync.delete_existing_expense(selected_category)
                                            elif Action == 0:
                                                running4 = True

                                        # Action
                                        except ValueError:
                                            print("\n-- Integers only --\n")
                                        except NonPlausibleInput:
                                            print("\n-- Selection only --\n")

                                elif Subcategory == 0:
                                    running3 = True

                            # Subcategory
                            except ValueError:
                                print("\n-- Integers only --\n")
                            except NonPlausibleInput:
                                print("\n-- Selection only --\n")

                            #####################################

                    elif Category == 0:
                        running2 = True

                # Category
                except ValueError:
                    print("\n-- Integers only --")
                except NonPlausibleInput:
                    print("\n-- Selection only --")

        ######## Income

        elif Inquiry == '2':

            while running2 == False:
                try:
                    Choice = int(input('\n--------------------\n'
                                       '\nIncome\n'
                                       '\n0 - Go back to main interface'
                                       '\n1 - Start income input process'
                                       '\nYour choice is: '))

                    if Choice == 1:
                        Income.income_insertion(sync.user_id)
                    elif Choice == 0:
                        running2 = True

                except ValueError:
                    print('Invalid input, returning to main interface')
                    running2 = True

        elif Inquiry == '3':
            while running2 == False:
                import base_calc
                base_calc.currency_conversion(sync.user_id)
                Report.report_creation(sync.user_id)
                print('Report created as PDF file, returning to main interface')
                running2 = True

        elif Inquiry == '4':
            while running2 == False:
                    unrec_transact.unrecorded_transact(sync.user_id)
                    print('Prediction created as PDF file, returning to main interface')
                    running2 = True

        elif Inquiry == '5':
            sys.exit()


