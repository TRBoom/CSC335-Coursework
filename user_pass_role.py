import pymysql, itertools
import random, string
from notifications import *
from get_connected import get_connected

def does_user_exist(username):
    con = get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT * from account where email = %s', (username))
        account_list = c.fetchall()
        if not account_list:
            return 0
        else:
            return 1
        
def id_list():
    con = get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT ID from account')
        account_list = list(itertools.chain(*c.fetchall()))
    return account_list
    
def user_add(fullname, username,ID, year, password, role):
    con = get_connected()
    with con:
        c = con.cursor()
        if not does_user_exist(username):
            sql = 'INSERT INTO account (name, email, ID, year, password, userType) VALUES (%s, %s, %s,%s, %s, %s)'
            val = (fullname, username,ID, year, password, role)
            c.execute(sql, val)
            con.commit()
            return 1
        else:
            return 0

def user_pass(username):
    con = get_connected()
    with con:
        c = con.cursor()
        if does_user_exist(username):
            c.execute('SELECT password from account where email = %s', (username))
            account_list = c.fetchall()
            return account_list[0][0]
                
def user_role(username):
    con = get_connected()
    with con:
        c = con.cursor()
        if does_user_exist(username):
            c.execute('SELECT userType from account where email = %s', (username))
            account_list = c.fetchall()
            return account_list[0][0]
      

def user_delete(username):
    con = get_connected()
    with con:
        c = con.cursor()
        if does_user_exist(username):
            c.execute('DELETE FROM account where email =%s', (username))
    return
            
def user_pass_change(username, new_password):
    con = get_connected()
    with con:
        c = con.cursor()
        if does_user_exist(username):
            c.execute('UPDATE account SET password = %s where email = %s', (new_password, username))
    return

def user_email_change(username, new_email):
    con = get_connected()
    with con:
        c = con.cursor()
        if does_user_exist(username):
            c.execute('UPDATE account SET email = %s where email = %s', (new_email, username))
    return

def user_class_change(username, new_class):
    con = get_connected()
    with con:
        c = con.cursor()
        if does_user_exist(username):
            c.execute('UPDATE account SET year = %s where email = %s', (new_class, username))
    return

def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """

    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

