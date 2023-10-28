import sqlite3

# Create a connection to the database
conn = sqlite3.connect('./stocks.db')

# Create a table
conn.execute('''CREATE TABLE prices (id integer primary key autoincrement, symbol text, price float, extraction_time datetime)''')


# Commit the changes and close the connection
conn.commit()
conn.close()