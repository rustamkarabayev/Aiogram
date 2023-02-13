import sqlite3
con = sqlite3.connect('translator.db')
cur = con.cursor()
cur.execute('''CREATE TABLE users (id VARCHAR(255), language VARCHAR(255))''')
