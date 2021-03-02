import csv
import pymysql

from get_connected import get_connected
    

con=get_connected()  
with con:
    c = con.cursor()
    c.execute("DROP TABLE IF EXISTS courses CASCADE;")
    table="CREATE TABLE courses ("
    table+="CRN         INT (5),"
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
    with open('Test_Schedule.csv', newline='') as csvfile: 
        reader = csv.DictReader(csvfile)
        for row in reader:
            temptuple=(row['CRN'], row['SUB'], row['CRSE'], row['SEC'], row['TITLE'], row['DAYS'], row['TIME'],
                row['INSTRUCTOR'], row['TYPE'], row['SEATS'], row['ENRL'])                     
            insert.append(temptuple)
    c.executemany(insert_query,insert)


print("Update Complete!")






