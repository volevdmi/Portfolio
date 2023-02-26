import sql_queries
from database import connection
import sql_queries

def clear_json():
    json_names = ["products", "user_portfolio", "user_signal", "user_watchlist", "users_id"]
    for name in json_names:
        f = open(f"{name}.json", 'w')
        f.close()
#clear_json()

def create_table():
    cursor = connection.cursor()
    cursor.execute(sql_queries.query_create_transactions_table())
    connection.commit()
    cursor.close()

#create_table()
