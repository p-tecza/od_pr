import sqlite3
from datetime import datetime
import uuid
from bcrypt import checkpw, hashpw, gensalt

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

def commit_new_restore(name, question, answer, gl_pep):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    code = str(uuid.uuid4())

    code_bytes=(code+gl_pep).encode('utf-8')
    code_hash=hashpw(code_bytes,gensalt())

    print(name)
    print(question)
    print(answer)
    print(code)

    conn.execute("""INSERT INTO RESTORE (NAME,CODE,QUESTION, ANSWER)
      VALUES (?,?,?,?)""",(name,code_hash,question,answer))
    conn.commit()
    conn.close()

    return code

def try_to_change_password(name,old,hash_new,gl_pep):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    # fetched=conn.execute("""SELECT PASS FROM USERS WHERE NAME=?""",(name,))
    # fetched_val=fetched.fetchall()[0][0]

    # print("name: "+name)
    # print("fval:",fetched_val)

    if checkpw((old+gl_pep).encode('utf-8'),get_pass_hashed(name)):
        conn.execute("""UPDATE USERS SET PASS=? WHERE NAME=?""",(hash_new,name,))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

def get_quest_for_user(name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    fetched=conn.execute("""SELECT QUESTION FROM RESTORE WHERE NAME=?""",(name,))
    check_fetch=fetched.fetchall()

    if len(check_fetch) == 0:
        conn.close()
        return "Error! No question provided for this user."
    print("fetch: ",check_fetch)
    print("len fetch: ",len(check_fetch))
    fetched_val=check_fetch[0][0]
    conn.close()
    return fetched_val

def check_if_answer_correct(name,answ,gl_pep):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    fetched=conn.execute("""SELECT ANSWER FROM RESTORE WHERE NAME=?""",(name,))
    check_fetch=fetched.fetchall()
    if len(check_fetch) == 0:
        conn.close()
        return False
    fetched_val=check_fetch[0][0]

    if checkpw((answ+gl_pep).encode('utf-8'),fetched_val):
        return True
    return False
    
def check_if_code_correct(name,code,gl_pep):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    fetched=conn.execute("""SELECT CODE FROM RESTORE WHERE NAME=?""",(name,))
    check_fetch=fetched.fetchall()
    if len(check_fetch) == 0:
        conn.close()
        return False
    fetched_val=check_fetch[0][0]

    if checkpw((code+gl_pep).encode('utf-8'),fetched_val):
        return True
    return False

def just_change_password(name,password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    conn.execute("""UPDATE USERS SET PASS=? WHERE NAME=?""",(password,name,))
    conn.commit()
    conn.close()


def check_if_already_friends(name,friend):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    fetched=conn.execute("""SELECT FRIEND FROM FRIENDS WHERE NAME=? AND FRIEND=?""",(name,friend,))
    check_fetch=fetched.fetchall()
    if len(check_fetch) == 0:
        conn.close()
        return False
    else:
        return True

def add_new_friend(name, friend):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    conn.execute("""INSERT INTO FRIENDS (NAME,FRIEND) VALUES (?,?)""",(name,friend))
    conn.commit()
    conn.close()
    return True

def get_friends(name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    fetched=conn.execute("""SELECT FRIEND FROM FRIENDS WHERE NAME=?""",(name,))
    friend_fetch=fetched.fetchall()
    friends=[]
    for x in friend_fetch:
        friends.append(x[0])
    return friends

def check_if_mutual_friends(name,friend):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    fetched=conn.execute("""SELECT FRIEND FROM FRIENDS WHERE NAME=? AND FRIEND=?""",(friend,name,))
    check_fetch=fetched.fetchall()
    print(check_fetch)
    if len(check_fetch) == 0:
        conn.close()
        return False
    elif len(check_fetch)==1:
        return True
