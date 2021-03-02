import csv,pymysql,itertools
from get_connected import get_connected


def wishlist_get(username):
    wishlist=[]
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('select wish from wishlist where email= %s', (username))
        wishlist = list(itertools.chain(*c.fetchall()))
    return wishlist

def wish_add(username, CRN):
    con=get_connected()
    with con:
        c = con.cursor()
        sql = 'insert into wishlist (email, wish) values (%s, %s)'
        val = (username, CRN)
        c.execute(sql,val)
        con.commit()

def wish_remove(username, CRN):
    con=get_connected()
    with con:
        c = con.cursor()
        sql = 'delete from wishlist where email=%s and wish=%s'
        val = (username, CRN)
        c.execute(sql,val)
        con.commit()
        
def wish_count():
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute("select WISH, count(*) AS 'num' from wishlist GROUP BY wish")
        count=c.fetchall()
    return dict(count)


def wish_count_append(some_tuples):
    some_lists=[]
    wishlist=wish_count()
    for tup in some_tuples:
        alist=list(tup)
        alist.append(wishlist.get(tup[4],0))
        some_lists.append(alist)
    return some_lists


