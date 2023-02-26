from datetime import date
from bs4 import BeautifulSoup
import lxml
import json_functions
import sql_queries
from database import connection
import requests


def get_price(product):
    try:
        url = "https://finance.yahoo.com/quote/"
        response = requests.get(str(url + product.upper()))
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('td', class_="Ta(end) Fw(600) Lh(14px)")
        print(quotes[0].text)
        return float(quotes[0].text)
    except:
        print("exception")
        return 0


def get_current_balance(user_id):
    user_portfolio = json_functions.read_json("user_portfolio")
    print(f"check {user_portfolio}")
    portfolio = user_portfolio[str(user_id)]
    print(portfolio.keys())
    current_balance = 0
    for item in portfolio.keys():
        print(item)
        price = get_price(item)
        if price != 0:
            current_balance += price * float(portfolio[item])
            print(f"curr balance: {current_balance}")
        else:
            return -1
    return current_balance


def get_real_balance(user_id):
    try:
        balance = 0
        cursor = connection.cursor()
        cursor.execute(sql_queries.query_get_real_balance(user_id))
        for row in cursor.fetchall():
            balance = row[0]
        cursor.close()
        return float(balance)
    except:
        print("exception")
        return -1


def check_input_signal(str):
    str_parts = str.split(" ")
    if len(str_parts) > 3:
        for part in str_parts:
            if part == " ":
                str_parts.remove(part)
    if len(str_parts) != 3:
        return -1  # error of input, less items that should be
    product = str_parts[0]
    min_price = str_parts[1]
    max_price = str_parts[2]
    products = json_functions.read_json("products")
    if product.upper() not in products:
        price = get_price(product)
        if price != -1:
            products.append(product.upper())
            json_functions.list_to_json(products, "products")
        else:
            return -2               # incorrect product
    if min_price > max_price:
        return -3
    return [product, min_price, max_price]

def check_input_transaction(str):
    str_parts = str.split(" ")
    if len(str_parts) > 3:
        for part in str_parts:
            if part == " ":
                str_parts.remove(part)
    if len(str_parts) != 3:
        return -1                    # error of input, less items that should be
    product = str_parts[0].replace(",", "")
    amount = str_parts[1].replace(",", ".")
    fact_price = str_parts[2].replace(",", ".")
    products = json_functions.read_json("products")
    if product.upper() not in products:
        price = get_price(product)
        if price != -1:
            products.append(product.upper())
            json_functions.list_to_json(products, "products")
        else:
            return -2               # incorrect product
    try:
        amount = float(amount)
        if amount == 0:
            return -3
    except:
        return -3                   #incorrect amount

    try:
        fact_price = float(fact_price)
        if fact_price < 0:
            return -4               #incorrect price
    except:
        return -4

    return [product.upper(), amount, fact_price]


def create_table():
    cursor = connection.cursor()
    cursor.execute(sql_queries.query_create_transactions_table())
    connection.commit()
    cursor.close()

#create_table()

def get_average_buy_price(user_id, product):
    try:
        cursor = connection.cursor()
        cursor.execute(sql_queries.query_get_average_buy_price(user_id, product))
        sum = 0
        amount = 0
        for row in cursor.fetchall():
            print(row[0], row[1])
            sum += float(row[0])*float(row[1])
            amount += float(row[1])
        cursor.close()
        if amount > 0:
            return sum/amount
        else:
            return 0
    except:
        cursor.close()
        return 0


def add_transaction(user_id, product, amount, price):
    user_portfolio = json_functions.read_json("user_portfolio")
    if product not in user_portfolio[str(user_id)].keys():
        user_portfolio[str(user_id)][product] = 0
    if amount + user_portfolio[str(user_id)][product] <= -1:
        return -1                      # user wants to sell more, than he has
    if amount < 0:  # sell product
        delta_price = round(get_average_buy_price(user_id, product) - price, 3)
        print(f"delta {delta_price}")
        balance = get_real_balance(user_id)
        balance -= get_average_buy_price(user_id, product) * user_portfolio[str(user_id)][product]
        balance += (-amount)*price
    else:
        balance = get_real_balance(user_id) + amount*price

    try:
        cursor = connection.cursor()
        print(user_id, product, amount, price, date.today(), balance)
        cursor.execute(sql_queries.query_add_transaction(user_id, product, amount, price, date.today(), balance))
        connection.commit()
        cursor.close()
        user_portfolio[str(user_id)][product] += amount
        json_functions.list_to_json(user_portfolio, "user_portfolio")
    except:
        return -2                      # error of adding to database
    return 1
