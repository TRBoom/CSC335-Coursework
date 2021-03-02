import csv
import pymysql, xlrd, os
import urllib.request
from notifications import notify_students
from get_connected import get_connected


def update_tables():
    con=get_connected()  
    c = con.cursor()
    '''
    #This section of comment is code to pull the schedule directly. Unfortunetly it's down. 
    url = 'https://storage.googleapis.com/csc330fa19/schedule.xlsx'
    urllib.request.urlretrieve(url, 'schedule.xlsx')
    wb = xlrd.open_workbook('schedule.xlsx')
    sh = wb.sheet_by_name('Schedule')
    with open('schedule.csv', 'w') as csvfile:
        wr = csv.writer(csvfile)
        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))
    '''
    c.execute("Delete from pre_courses;")
    c.execute("INSERT INTO pre_courses (CRN, Subject, Course, Section, Title, Days, Time, Instructors, Type, Seats, Enrollment) SELECT CRN, Subject, Course, Section, Title, Days, Time, Instructors, Type, Seats, Enrollment FROM courses;")
    c.execute("Delete from courses;")
    insert=[]
    insert_query = """INSERT INTO courses (CRN, Subject, Course, Section, Title, Days, Time, Instructors, Type, Seats, Enrollment) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    with open('Schedule.csv', newline='') as csvfile: 
        reader = csv.DictReader(csvfile)
        for row in reader:
            temptuple=(row['CRN'], row['SUB'], row['CRSE'], row['SEC'], row['TITLE'], row['DAYS'], row['TIME'],
                row['INSTRUCTOR'], row['TYPE'], row['SEATS'], row['ENRL'])
                      
            insert.append(temptuple)
    c.executemany(insert_query,insert)
    os.remove("schedule.xlsx")
    os.remove("schedule.csv")
    print("Update Complete!")
    return

def cancelled_classes():
    con=get_connected()  
    c = con.cursor()
    c.execute("SELECT distinct p.CRN FROM  pre_courses p left outer join courses c on p.CRN=c.CRN where c.CRN is null;")
    for row in c.fetchall():
        c.execute("SELECT email, course FROM  courselist where course = %s", (row))
        for row in c.fetchall():
            notify_students(row[0],str(row[1]),'2')
    return

def new_Section():
    con=get_connected()  
    c = con.cursor()
    c.execute("SELECT distinct c.CRN, c.Title FROM  courses c left outer join pre_courses p on c.CRN=p.CRN where p.CRN is null;")
    for row in c.fetchall():
        c.execute("SELECT distinct CRN FROM  pre_courses where Title = %s", (row[1]))
        for row in c.fetchall():
            c.execute("SELECT email, wish FROM  wishlist where wish = %s", (row))
            for row in c.fetchall():
                      notify_students(row[0],str(row[1]),'0')
    return

def updated_seats():
    con=get_connected()  
    c = con.cursor()
    c.execute("SELECT distinct c.CRN FROM  courses c left outer join pre_courses p on c.CRN=p.CRN && c.Instructors=p.Instructors where (c.Enrollment <> p.Enrollment || c.Seats <> p.Seats) && (c.Enrollment < c.Seats);")
    for row in c.fetchall():
        c.execute("SELECT email, wish FROM  wishlist where wish = %s", (row))
        for row in c.fetchall():
            notify_students(row[0],str(row[1]),'1')
    return

def updated_year(year):
    con=get_connected()  
    c = con.cursor()
    c.execute("SELECT distinct CRN FROM courses where Enrollment < Seats);")
    for row in c.fetchall():
        c.execute("SELECT a.email, wish, a.year FROM  wishlist w INNER JOIN account a ON w.email = a.email AND a.year = %s where wish = %s", (year,row))
        for row in c.fetchall():
            notify_students(row[0],str(row[1]),'1')
    return        

def classes_at_risk():
    con=get_connected()  
    c = con.cursor()
    c.execute("SELECT distinct c.CRN FROM  courses c left outer join pre_courses p on c.CRN=p.CRN && c.Instructors=p.Instructors where (c.Enrollment <> p.Enrollment || c.Seats <> p.Seats) && (c.Enrollment < (c.Seats*4)/10);")
    for row in c.fetchall():
        c.execute("SELECT email, course FROM  courselist where course = %s", (row))
        for row in c.fetchall():
            notify_students(row[0],str(row[1]),'3')
    return 
