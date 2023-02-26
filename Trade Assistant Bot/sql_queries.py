def query_create_transactions_table():
    return f'''
    CREATE TABLE IF NOT EXISTS transactions(
        transaction serial,
        user_id VARCHAR(20),
        product VARCHAR(50) ,
        amount NUMERIC , 
        price NUMERIC, 
        date DATE, 
        real_balance NUMERIC DEFAULT 0
    );
    '''


def query_add_transaction(user_id, product, amount, price, date, balance):
    return f'''
    INSERT INTO transactions
    (user_id, product, amount, price, date, real_balance)
    VALUES('{user_id}', '{product}', {amount}, {price}, '{date}', {balance});
    '''

def query_get_real_balance(user_id):
    return f'''
    SELECT real_balance FROM transactions WHERE user_id = '{user_id}' 
    ORDER BY transaction DESC LIMIT 1;    
    '''

def query_get_average_buy_price(user_id, product):
    return f'''
    SELECT price, amount FROM transactions WHERE user_id = '{user_id}' AND amount > 0 AND product = '{product}';
    '''