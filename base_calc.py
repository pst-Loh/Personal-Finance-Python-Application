import sqlite3
from datetime import datetime
import pandas as pd
import json
import requests


def currency_conversion(user_id):

    # fixer.io
    API_KEY = '5b1310686e540f2e3d61505f5d391759'
    # date
    date_today = datetime.now()
    date_today_sql_compare = date_today.strftime("%Y%m%d")

    # SQL connect
    with sqlite3.connect("{user_id}.sqlite".format(user_id=user_id)) as conn:
        cursor = conn.cursor()

#### Retrieving itemID, transactionID, currency, date and amount from the database ####

    ######

#### Retrieving itemIDs where currency conversion has not taken place yet
    itemIDs = cursor.execute('SELECT itemID FROM TransactionItems WHERE [baseAmount] IS NULL')
    itemIDs_table = []
    for tuple in itemIDs:
        for element in tuple:
            itemIDs_table.append(element)
    if len(itemIDs_table) > 0:
        print('\n--- Currency conversion performed due to '+str(len(itemIDs_table))+' new entries. ---')
    else:
        print('\n--- No currency conversion performed as regards new entries. ---')

################################### Retrieving itemIDs of - to be updated - baseamounts of future expenses/income
    # Retrieving all transactionIDs
    all_trans = []
    tuple_all_trans = cursor.execute('SELECT [transactionID] FROM Transactions')
    for tuple in tuple_all_trans:
        for element in tuple:
            all_trans.append(element)

    # Getting all dates corresponding to all transactionIDs
    all_trans_dates = []
    for atd in all_trans:
        tuple_save_all_dates = cursor.execute('SELECT [date] FROM Transactions WHERE [transactionID] IS ('+str(atd)+')')
        for tuple in tuple_save_all_dates:
            for element in tuple:
                all_trans_dates.append(element)

    # Transforming date format
    all_dates_comparable_format = []
    for date in all_trans_dates:
        # formatting into a better comparable value
        comparable_format = datetime.strptime(date, "%d.%m.%Y").strftime('%Y%m%d')
        all_dates_comparable_format.append(comparable_format)

    # Create dataframe for all formatted dates with transactionIDs
    dataframe3 = pd.DataFrame({"date": all_trans_dates,
                               "date_formatted": all_dates_comparable_format,
                               "transactionID": all_trans,})

    # Compare dates and filter today/future dates as regards transactionIDs
    date_update_trans = []
    for i in range(0, len(dataframe3), 1):
        if int(date_today_sql_compare) <= int(dataframe3.date_formatted[i]):
            date_update_trans.append(dataframe3.transactionID[i])

    # Extend list of itemIDs according to transactionIDs that need to be updated due to future values
    length_new_entries = len(itemIDs_table)
    for i in date_update_trans:
        itemIDs2 = cursor.execute('SELECT itemID FROM TransactionItems WHERE [transactionID] IS ('+str(i)+')')
        for tuple in itemIDs2:
            for element in tuple:
                if element not in itemIDs_table:
                    itemIDs_table.append(element)
    length_future_values = len(itemIDs_table)-length_new_entries


    if length_future_values > 0:
        print('\n--- Currency conversion performed due to ' + str(length_future_values) + ' future amounts. ---')
    else:
        print('\n--- No currency conversion performed as regards open future amounts. ---')

###################################### Retrieving ItemIDs of recently changed entries (for case of amount change)

    # Days of consideration set here
    days_back_consid = 2

    # Retrieve all update-dates according to transactionIDs
    all_trans_updates = []
    for atd in all_trans:
        tuple_save_all_updates = cursor.execute('SELECT [updated] FROM Transactions WHERE [transactionID] IS ('+str(atd)+')')
        for tuple in tuple_save_all_updates:
            for element in tuple:
                all_trans_updates.append(element)

    #  Formatting of date
    all_updates_comparable_format = []
    for date in all_trans_updates:
        # formatting into a better comparable value
        comparable_format_2 = datetime.strptime(date, "%d.%m.%Y %H:%M:%S").strftime('%Y%m%d')
        all_updates_comparable_format.append(comparable_format_2)

    # Create dataframe for all formatted updates with transactionIDs
    dataframe3_2 = pd.DataFrame({"date": all_trans_updates,
                               "date_formatted": all_updates_comparable_format,
                               "transactionID": all_trans,})

    # Comparison taking into account updated-dates from the past depending on the days set above
    update_trans = []
    for i in range(0, len(dataframe3_2), 1):
        if int(date_today_sql_compare)-days_back_consid <= int(dataframe3_2.date_formatted[i]):
            update_trans.append(dataframe3_2.transactionID[i])

    # print(update_trans)
    # Extend list of itemIDs according to update-dates in order to update post changed amounts

    for i in update_trans:
        itemIDs3 = cursor.execute('SELECT itemID FROM TransactionItems WHERE [transactionID] IS ('+str(i)+')')
        for tuple in itemIDs3:
            for element in tuple:
                if element not in itemIDs_table:
                    itemIDs_table.append(element)

    length_recent_act = len(itemIDs_table)-length_future_values-length_new_entries
    if length_recent_act > 0:
        print('\n--- Currency conversion performed due to ' + str(length_recent_act) + ' recent changes in entries. ---\n')
    else:
        print('\n--- No currency conversion performed as regards recent changes in entries. ---\n')


    # print(itemIDs_table)
###################################### All ItemIDs check

    # Retrieving the respective transactionIDs
    item_trans = []
    for i in itemIDs_table:
        tuple_save = cursor.execute('SELECT [transactionID] FROM TransactionItems WHERE [itemID] IS ('+str(i)+')')
        for tuple in tuple_save:
            for element in tuple:
                if element not in item_trans:   # hier eigtl nicht notwendig
                    item_trans.append(element)

    print(item_trans)

    # Retrieving respective dates
    date = []
    for d in item_trans:
        tuple_save = cursor.execute('SELECT [date] FROM Transactions WHERE [transactionID] IS ('+str(d)+')')
        for tuple in tuple_save:
            for element in tuple:
                date.append(element)

    print(date)

    # Retrieving respective currencies
    transID_currency = []
    for c in item_trans:
        tuple_save = cursor.execute('SELECT [currency] FROM Transactions WHERE [transactionID] IS ('+str(c)+')')
        for tuple in tuple_save:
            for element in tuple:
                transID_currency.append(element)


    # Retrieving personal expense
    owed_share = []
    for s in item_trans:
        tuple_save = cursor.execute('SELECT [amount] FROM TransactionItems WHERE [transactionID] IS ('+str(s)+')')
        for tuple in tuple_save:
            for element in tuple:
                owed_share.append(element)

    print(len(owed_share))
    print(len(date))
    print(len(transID_currency))
    print(len(itemIDs_table))
    print(len(item_trans))

    # Creating dataframe for further processing
    dataframe = pd.DataFrame({"itemID": itemIDs_table,
                              "transactionID": item_trans,
                              "owed_share": owed_share,
                              "currency": transID_currency,
                              "date": date,
                              })

    print(dataframe)
    baseAmount = []
    for i in range(0, len(dataframe), 1):
        # Date adjustments for the API request
        date_required = dataframe.date[i]
        date_required_formatted = datetime.strptime(date_required, "%d.%m.%Y").strftime("%Y-%m-%d")
        date_today_formatted = date_today.strftime("%Y-%m-%d")

        # Amounts in EUR remain the same
        if dataframe.currency[i] == 'EUR':
            baseAmount.append(dataframe.owed_share[i])

        # Checking for currencies deviating from EUR
        elif dataframe.currency[i] != 'EUR':

                # Retrieving latest currency rates as for today and future values
            if date_today_formatted < date_required_formatted:
                response = requests.get("http://data.fixer.io/api/latest?access_key="+API_KEY)
                currency_rates = json.loads(response.text)
                conversion_rate = currency_rates["rates"][str(dataframe.currency[i])]

                # converting own share
                currency_conversion_exp = round(float(dataframe.owed_share[i])/conversion_rate, 1)
                # update new currency
                baseAmount.append(currency_conversion_exp)

            else:
                # retrieving historical currency rates
                response = requests.get("http://data.fixer.io/api/" + date_required_formatted + "?access_key="+API_KEY)
                currency_rates = json.loads(response.text)
                # looking for the base rate entered on splitwise
                conversion_rate = currency_rates["rates"][str(dataframe.currency[i])]
                # converting own share
                currency_conversion_exp = round(float(dataframe.owed_share[i])/conversion_rate, 1)
                # update new currency
                baseAmount.append(currency_conversion_exp)

    # Includes the converted currencies
    dataframe2 = pd.DataFrame({"itemID": itemIDs_table,
                              "transactionID": item_trans,
                              "owed_share": owed_share,
                              "baseAmount": baseAmount,
                              "currency": transID_currency,
                              "date": date,
                              })

    # Updating the database by the converted base amounts in EUR
    with conn:
        for i in range(0, len(dataframe2), 1):
            cursor.execute('UPDATE TransactionItems SET baseAmount = (' + str(dataframe2.baseAmount[i]) + ') WHERE transactionID = (' + str(dataframe2.transactionID[i]) + ')')
            #cursor.execute('UPDATE TransactionItems SET baseAmount = ('+str(dataframe2.baseAmount[i])+') WHERE transactionID = ('+str(dataframe2.transactionID[i])+')')

    print(dataframe2)
    return dataframe2


# currency_conversion(user_id)

