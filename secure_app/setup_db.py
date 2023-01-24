import sqlite3

conn = sqlite3.connect('users.db')
print("Opened database successfully")

# conn.execute('''CREATE TABLE USERS
#          (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#          NAME TEXT NOT NULL,
#          PASS TEXT NOT NULL,
#          BAD_LOGIN INTEGER NOT NULL,
#          UNLOCK_DATE DATETIME NOT NULL,
#          BLOCK_MULTIPLIER INTEGER NOT NULL);''')

# # print("Table created successfully")


# conn.execute('''CREATE TABLE FRIENDS
#          (ID INTEGER PRIMARY KEY AUTOINCREMENT,
#          NAME TEXT NOT NULL,
#          FRIEND TEXT NOT NULL);''')

# # conn.execute("INSERT INTO USERS (NAME,PASS,BAD_LOGIN, UNLOCK_DATE) \
# #       VALUES ('Paul','giga tajne',0,DATETIME('now'))")



# conn.execute('''CREATE TABLE RESTORE (ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME TEXT NOT NULL,CODE TEXT NOT NULL,QUESTION TEXT NOT NULL,ANSWER TEXT NOT NULL)''')

# # conn.execute("INSERT INTO RESTORE (NAME,CODE,QUESTION, ANSWER) \
# #       VALUES ('user','1337','co?','to')")

conn.commit()


cursor=conn.execute("SELECT * FROM FRIENDS")

for row in cursor:
    print(row)


conn.close()

