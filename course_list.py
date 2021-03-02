import csv,pymysql,itertools
from get_connected import get_connected


def courselist_get(username):
    courselist=[]
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('select course from courselist where email= %s', (username))
        courselist = list(itertools.chain(*c.fetchall()))
    return courselist

def course_add(username, CRN):
    con=get_connected()
    with con:
        c = con.cursor()
        sql = 'insert into courselist (email, course) values (%s, %s)'
        val = (username, CRN)
        c.execute(sql,val)
        con.commit()
    return

def course_remove(username, CRN):
    con=get_connected()
    with con:
        c = con.cursor()
        sql = 'delete from courselist where email=%s and course=%s'
        val = (username, CRN)
        c.execute(sql,val)
        con.commit()
    return



