import pymysql

#Change the information here to connect to your database.        
def get_connected():
    #Format====IP-USER-PASSWORD-DATABASE
    return pymysql.connect('IP ADDRESS', 'username', 'password', 'database')
        





