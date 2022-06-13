import datetime
from polls.models import Inforlession, Lesson, Student, User
from django.db import connections
cursor = connections['default'].cursor()

def getListLessonOnTimeOfTeacher(idTeacher,keySearch,time):
    # time = datetime.datetime.today().strftime('%d/%m/%Y')
    # time test : "27/05/2022" ;  keySearch = "ối"
    sql = """
    SELECT lesson.idClasses,lesson.idSubject,classes.name as nameClasses,
    subject.name as nameSubject, subject.codeSubject as codeSubject,
    lesson.timeStart, lesson.timeEnd,lesson.id as idLesson
    FROM lesson,classes,subject,teacher where
    lesson.idTeacher = %s and
    lesson.idClasses=classes.id 
    and lesson.idSubject = subject.id
    and lesson.idTeacher = teacher.id
    and ( date(lesson.timeStart)<= %s and date(lesson.timeEnd) >=%s)
    """
    if keySearch is not None:
        sql+="and subject.name like %s"
        cursor.execute(sql,[idTeacher,time,time,"%"+keySearch+"%"])
    else: 
        cursor.execute(sql,[idTeacher,time,time])
    rows = cursor.fetchall()
    return rows

def countNumberStudentByIdLesson(idLesson):
    sql = "select count(id) as numberStudent from inforlession where idLession =%s"
    cursor.execute(sql,[idLesson])
    result = cursor.fetchone()
    return result[0]

def getListStudentOfLession(idLesson):
    sql = """select * from inforlession
    LEFT JOIN (
    SELECT student.id as idStudent,student.codeStudent,student.idUser,
    user.username,user.email,user.fullname,user.address,user.phone,user.image,user.role
    FROM student
    LEFT JOIN user ON student.idUser = user.id) as inforStudentTemp ON inforStudentTemp.idStudent = inforlession.idStudent
    where inforlession.idLession=%s"""
    cursor.execute(sql,[idLesson])
    rows = cursor.fetchall()
    return rows

def getInforLesson(idLesson):
    sql = """  
    SELECT lesson.idClasses,lesson.idSubject,classes.name as nameClasses,
    subject.name as nameSubject, subject.codeSubject as codeSubject,
    lesson.timeStart, lesson.timeEnd ,lesson.description,lesson.id as idLesson,
    user.image, user.fullname
    FROM lesson,classes,subject,teacher,user where
    lesson.id=%s and
    lesson.idClasses=classes.id 
    and lesson.idSubject = subject.id
    and lesson.idTeacher = teacher.id
    and teacher.idUser = user.id ; 
    """
    cursor.execute(sql,[idLesson])
    result = cursor.fetchone()
    return result

def addNewLesson(lesson,listIdStudent):
    lesson.save()
    newLessonInsert = Lesson.objects.all().last()
    for idStudent in listIdStudent:
        student = Student.objects.get(id=idStudent)
        inforLesson = Inforlession(status_attendance="Chưa điểm danh",idlession=newLessonInsert, idstudent=student)
        inforLesson.save()


def getListSubject():
    sql = """select * from subject """
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows