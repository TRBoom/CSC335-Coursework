import pymysql, itertools
from wish_list import *
from get_connected import get_connected
       

def course_get(CRN):
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT Title,Subject,Course,Section,CRN,Enrollment,Seats from courses where CRN = %s', (CRN))
        course = c.fetchall()
        return wish_count_append(set(course))
    
def course_valid():
    valid=[]
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT CRN from courses')
        valid = list(itertools.chain(*c.fetchall()))
        return valid

def course_invalid():
    invalid=[]
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT CRN from courses where Enrollment<Seats')
        invalid = list(itertools.chain(*c.fetchall()))
        return invalid


def subject_valid():
    valid=[]
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT Subject from courses')
        valid = list(itertools.chain(*c.fetchall()))
        return list(set(valid))


def class_valid():
    valid=[]
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT Course from courses')
        valid = list(itertools.chain(*c.fetchall()))
        return list(set(valid))
    

def section_valid():
    valid=[]
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT Section from courses')
        valid = list(itertools.chain(*c.fetchall()))
        return list(set(valid))


def courseName_valid():
    valid=[]
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT CONCAT(Subject,Course) from courses')
        valid = list(itertools.chain(*c.fetchall()))
        return valid

def courseName_get(SUBCRSE):
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT Title,Subject,Course,Section,CRN,Enrollment,Seats from courses where CONCAT(Subject,Course) = %s',
                  (SUBCRSE))
        course_list = c.fetchall()
        return wish_count_append(set(course_list))


def subject_get(SUB):
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT Title,Subject,Course,Section,CRN,Enrollment,Seats from courses where Subject = %s',
                  (SUB))
        course_list = c.fetchall()
        return wish_count_append(set(course_list))


def faculty_lookup(SUB, course, SEC):
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT CRN from courses where Subject = %s AND Course= %s AND Section= %s',
                  (SUB, course, SEC))
        CRN = c.fetchall()[0][0]
        c.execute('select email from wishlist where wish= %s', (CRN))
        wishers = list(itertools.chain(*c.fetchall()))
        course_report=[]
        for wisher in wishers:
            c.execute('select name,email,year,id from account where email= %s', (wisher))
            course_report.append(c.fetchall()[0])
        return course_report
    
    
def title_get(CRN):
    con=get_connected()
    with con:
        c = con.cursor()
        c.execute('SELECT Title from courses where CRN = %s', (CRN))
        course = c.fetchall()
        return course[0][0]

