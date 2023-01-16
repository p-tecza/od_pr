import sqlite3
from datetime import datetime

def check_if_username_exists(name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    fetched_name=conn.execute("""SELECT NAME FROM USERS WHERE NAME=?""",(name,))
    return not len(fetched_name.fetchall()) == 0

def create_new_user(name,password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    try:
        conn.execute("""INSERT INTO USERS (NAME, PASS, BAD_LOGIN, UNLOCK_DATE, BLOCK_MULTIPLIER)
         VALUES (?,?,?,?,?)""",(name,password,0,datetime.now(),1))
        conn.commit()
        conn.close()
    except:
        print("PROBLEM CREATE NEW USER")
        return False
    return True

def login_attempt(name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    fetched_num=0
    try:
        fetched=conn.execute("""SELECT * FROM USERS WHERE NAME=?""",(name,))
        fetched_num=len(fetched.fetchall())
        conn.close()
    except:
        print("PROBLEM LOGIN ATTEMPT")
        return False
    
    if fetched_num == 1:
        return True
    else:
        return False

def get_pass_hashed(name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    fetched=conn.execute("""SELECT PASS FROM USERS WHERE NAME=?""",(name,))
    
    fetched_val=fetched.fetchall()[0][0]
    conn.close()
    return fetched_val
    
def increment_bad_login_spree(name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    fetched=conn.execute("""SELECT BAD_LOGIN FROM USERS WHERE NAME=?""",(name,))
    print(conn.execute("""SELECT BAD_LOGIN FROM USERS WHERE NAME=?""",(name,)).fetchall())
    fetched_val=int(fetched.fetchall()[0][0])
    fetched_val+=1
    if fetched_val>3:
        conn.execute("""UPDATE USERS SET BAD_LOGIN=? WHERE NAME=?""",(0,name,))
        conn.commit()
        conn.close()
        return fetched_val
    conn.execute("""UPDATE USERS SET BAD_LOGIN=? WHERE NAME=?""",(fetched_val,name,))
    conn.commit()
    conn.close()
    return fetched_val

def reset_bad_login_counter(name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    conn.execute("""UPDATE USERS SET BAD_LOGIN=? WHERE NAME=?""",(0,name,))
    conn.commit()
    conn.close()

def check_if_banned(name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    fetched=conn.execute("""SELECT UNLOCK_DATE FROM USERS WHERE NAME=?""",(name,))
    fetched_val=fetched.fetchall()[0][0]
    fetched_val=fetched_val.split(".")[0]
    datetime_object = datetime.strptime(fetched_val, '%Y-%m-%d %H:%M:%S')
    date_now=str(datetime.now()).split(".")[0]
    date_now=datetime.strptime(date_now, '%Y-%m-%d %H:%M:%S')
    roznica=int(datetime_object.timestamp())-int(date_now.timestamp())
    print("roznica: ",roznica)
    if roznica<0:
        conn.close()
        return False
    conn.close()
    return True

def ban_account_for_minutes(name,duration):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    date_now=str(datetime.now()).split(".")[0]
    date_now=datetime.strptime(date_now, '%Y-%m-%d %H:%M:%S')
    basic_timestamp=date_now.timestamp()
    fetched=conn.execute("""SELECT BLOCK_MULTIPLIER FROM USERS WHERE NAME=?""",(name,))
    fetched_val=int(fetched.fetchall()[0][0])
    banned_timestamp=basic_timestamp+duration*60*fetched_val
    locked_date=datetime.fromtimestamp(banned_timestamp)
    conn.execute("""UPDATE USERS SET UNLOCK_DATE=? WHERE NAME=?""",(locked_date,name,))
    fetched_val+=1
    conn.execute("""UPDATE USERS SET BLOCK_MULTIPLIER=? WHERE NAME=?""",(fetched_val,name,))
    conn.commit()

    return locked_date