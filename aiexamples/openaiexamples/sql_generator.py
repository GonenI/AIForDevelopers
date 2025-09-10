import sqlite3
from sqlite3 import Error

path = "mydatabase.db"

connection = None
try:
    connection = sqlite3.connect(path)
    print("Connection to SQLite DB successful")
except Error as e:
    print(f"The error '{e}' occurred")

# Create the users table
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER)
  """  # Added closing parenthesis here

# create the orders table
create_orders_table = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    product TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id))
    """  # Added closing parenthesis here

# send the SQL query to the database
connection.execute(create_users_table)
connection.execute(create_orders_table)
# add some sample users and orders
connection.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
connection.execute("INSERT INTO users (name, age) VALUES ('Bob', 35)")
connection.execute("INSERT INTO orders (date, product, user_id) VALUES ('2022-01-01','shoes', 1)")
connection.execute("INSERT INTO orders (date, product, user_id) VALUES ('2022-01-02','purse', 2)")
connection.execute("INSERT INTO orders (date, product, user_id) VALUES ('2022-01-03','earings', 2)")
# commit the changes
connection.commit()
# fetch the data from the database
cursor = connection.cursor()

from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {
      "role": "user",
      "content": "Given the following SQL tables:\n" 
      + create_users_table + "\n" + create_orders_table + "\n"
      "Write only an SQL query which retrieves all the orders for users whose name starts with A. Return only the query, without any additional information."
    }
  ],
  temperature=0.7,
  max_tokens=64,
  top_p=1
)

actualResponse = response.choices[0].message.content
print("SQL Query: ")
print(actualResponse)

cursor.execute(actualResponse)   
users = cursor.fetchall()
print("SQL Response:\n")
for user in users:
    print(user)

# close the connection
connection.close()


    