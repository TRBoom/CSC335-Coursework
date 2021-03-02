import csv
import pymysql, xlrd, os
import urllib.request

from get_connected import get_connected
con=get_connected()  
url = 'https://storage.googleapis.com/csc330fa19/schedule.xlsx'
urllib.request.urlretrieve(url, 'schedule.xlsx')
wb = xlrd.open_workbook('schedule.xlsx')
sh = wb.sheet_by_name('Schedule')
with open('schedule.csv', 'w') as csvfile:
    wr = csv.writer(csvfile)
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
with con:
    c = con.cursor()
    #Creates the course table
    c.execute("DROP TABLE IF EXISTS courses CASCADE;")
    table="CREATE TABLE courses ("
    table+="CRN         INT,"
    table+="Subject     VARCHAR (255),"
    table+="Course      VARCHAR (255),"
    table+="Section     VARCHAR (255),"
    table+="Title       VARCHAR (255),"
    table+="Days        VARCHAR (255),"
    table+="Time        VARCHAR (255),"
    table+="Instructors VARCHAR (255),"
    table+="Type        VARCHAR (255),"
    table+="Seats       INT,"
    table+="Enrollment  INT);"
    c.execute(table)
    insert=[]
    insert_query = """INSERT INTO courses (CRN, Subject, Course, Section, Title, Days, Time, Instructors, Type, Seats, Enrollment) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    with open('schedule.csv', newline='') as csvfile: 
        reader = csv.DictReader(csvfile)
        for row in reader:
            temptuple=(row['CRN'], row['SUB'], row['CRSE'], row['SEC'], row['TITLE'], row['DAYS'], row['TIME'],
                row['INSTRUCTOR'], row['TYPE'], row['SEATS'], row['ENRL'])                    
            insert.append(temptuple)
    c.executemany(insert_query,insert)
    #Creates the course history table
    c.execute("DROP TABLE IF EXISTS pre_courses CASCADE;")
    table="CREATE TABLE pre_courses ("
    table+="CRN         INT,"
    table+="Subject     VARCHAR (255),"
    table+="Course      VARCHAR (255),"
    table+="Section     VARCHAR (255),"
    table+="Title       VARCHAR (255),"
    table+="Days        VARCHAR (255),"
    table+="Time        VARCHAR (255),"
    table+="Instructors VARCHAR (255),"
    table+="Type        VARCHAR (255),"
    table+="Seats       INT,"
    table+="Enrollment  INT);"
    c.execute(table)
    insert=[]
    insert_query = """INSERT INTO courses (CRN, Subject, Course, Section, Title, Days, Time, Instructors, Type, Seats, Enrollment) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    with open('schedule.csv', newline='') as csvfile: 
        reader = csv.DictReader(csvfile)
        for row in reader:
            temptuple=(row['CRN'], row['SUB'], row['CRSE'], row['SEC'], row['TITLE'], row['DAYS'], row['TIME'],
                row['INSTRUCTOR'], row['TYPE'], row['SEATS'], row['ENRL'])                      
            insert.append(temptuple)
    c.executemany(insert_query,insert)
    #Creates the Course watch table
    c.execute("DROP TABLE IF EXISTS courselist CASCADE;")
    table="CREATE TABLE courselist ("
    table+="email         VARCHAR (255),"
    table+="course      INT);"
    c.execute(table)
    #Creates Account Table
    c.execute("DROP TABLE IF EXISTS account CASCADE;")
    table="CREATE TABLE account ("
    table+="name         VARCHAR (255),"
    table+="email     VARCHAR (255),"
    table+="id     VARCHAR (255),"
    table+="year     VARCHAR (255),"
    table+="password      VARCHAR (255),"
    table+="userType     VARCHAR (1));"
    c.execute(table)
    #Creates the wish list table
    c.execute("DROP TABLE IF EXISTS wishlist CASCADE;")
    table="CREATE TABLE wishlist ("
    table+="email         VARCHAR (255),"
    table+="wish      INT);"
    c.execute(table)




os.remove("schedule.xlsx")
os.remove("schedule.csv")
print("All tables made!")






