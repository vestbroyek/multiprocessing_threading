import sqlite3

# Create a connection to the database
conn = sqlite3.connect('stocks.db')

# Create a table
conn.execute('''CREATE TABLE prices (id serial primary key, symbol text, price real, extraction_time timestamp)''')


# Commit the changes and close the connection
conn.commit()
conn.close()