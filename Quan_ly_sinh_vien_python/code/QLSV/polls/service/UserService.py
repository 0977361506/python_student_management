import datetime
from polls.models import User
from django.db import connections
cursor = connections['default'].cursor()

def getListStudent(keySearch):
    sql = """
    SELECT student.id as idStudent,student.codeStudent,student.idUser,
    user.username,user.email,user.fullname,user.address,user.phone,user.image,user.role
    FROM student
    LEFT JOIN user ON student.idUser = user.id
    """
    if keySearch is not None:
        sql+="where  user.fullname like  %s"
        cursor.execute(sql,["%"+keySearch+"%"])
    else:
        cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def getListTeacher(keySearch):
    sql = """
    SELECT teacher.id as idTeacher,teacher.codeTeacher,teacher.idUser,
    user.username,user.email,user.fullname,user.address,user.phone,user.image,user.role
    FROM teacher
    LEFT JOIN user ON teacher.idUser = user.id
    """
    if keySearch is not None:
        sql+="where  user.fullname like  %s"
        cursor.execute(sql,["%"+keySearch+"%"])
    else:
        cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

def registerStudent(newuser,codeStudent) :
    newuser.save()
    newUserInsert = User.objects.all().last()
    cursor.execute('''INSERT INTO student (idUser,codeStudent)  VALUES (%s,%s)''',[newUserInsert.id,codeStudent])

def registerTeacher(newuser,codeTeacher) :
    newuser.save()
    newUserInsert = User.objects.all().last()
    cursor.execute('''INSERT INTO teacher (idUser,codeTeacher)  VALUES (%s,%s)''',[newUserInsert.id,codeTeacher])

def editStudent(idStudent,codeStudent) :
    cursor.execute('''UPDATE student SET codeStudent = %s where id=%s''',[codeStudent,idStudent])

def editTeacher(idTeacher,codeTeacher) :
    cursor.execute('''UPDATE teacher SET codeTeacher = %s where id=%s''',[codeTeacher,idTeacher])

def editUser(idUser,username,fullname,phone,email,address,image) :
    if(image==None):
        cursor.execute('''UPDATE user SET username = %s,fullname=%s,phone=%s,email=%s,address=%s
         where id=%s''',[username,fullname,phone,email,address,idUser])
    else:
        cursor.execute('''UPDATE user SET username = %s,fullname=%s,phone=%s,email=%s,address=%s,image=%s
         where id=%s''',[username,fullname,phone,email,address,image,idUser])

def getListTeacherNotInTime(timeStart,timeEnd):
    #example : "2022-05-27 03:14:07" and "2022-05-27 05:14:07"
    sql = """
    select temp1.id as idTeacher, user.fullname
    from (select * from teacher where id not in (SELECT distinct(idTeacher) FROM lesson where timeStart between %s and %s or
    timeEnd between %s and %s)) as temp1 
    left join user
    on temp1.idUser = user.id
    """
    cursor.execute(sql,[timeStart,timeEnd,timeStart,timeEnd])
    rows = cursor.fetchall()
    return rows