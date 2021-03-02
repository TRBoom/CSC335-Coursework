import csv
import pymysql
from database_updates import *
from get_connected import get_connected
    

con=get_connected()  
with con:
    c = con.cursor()

    c.execute("Delete from pre_courses;")
    c.execute("INSERT INTO pre_courses (CRN, Subject, Course, Section, Title, Days, Time, Instructors, Type, Seats, Enrollment) SELECT CRN, Subject, Course, Section, Title, Days, Time, Instructors, Type, Seats, Enrollment FROM courses;")
    c.execute("Delete from courses;")
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


print("Course Table Updated!")
updated_seats()
cancelled_classes()
new_Section()
classes_at_risk()




