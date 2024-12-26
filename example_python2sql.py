import sqlite3

#Establish a connection and cursor
connection=sqlite3.connect("data1_db.db")
cursor=connection.cursor()

#Query all columns
cursor.execute("SELECT * from events")
rows=cursor.fetchall()

#Insert new rows
new_rows=[('Bombay', 'Mumbai City', '5.5.2024'),
          ('Varanasi', 'Banaras City', '15.5.2025')]

cursor.executemany("INSERT into events VALUES(?,?,?)",new_rows)
connection.commit()

