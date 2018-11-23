import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS books(title text, author text)"
cursor.execute(create_table)

cursor.execute("INSERT INTO books VALUES ('merda','testing')")

connection.commit()
connection.close()
