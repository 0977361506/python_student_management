from polls.models import Classes
from django.db import connections
cursor = connections['default'].cursor()

def getListClasses(keySearch):
    sql = """
    SELECT * FROM classes
    """
    if keySearch is not None:
        sql+="where  classes.name like  %s"
        cursor.execute(sql,["%"+keySearch+"%"])
    else:
        cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


def registerClasses(newClass) :
    newClass.save()

def editClasses(idClass,name,description) :
    cursor.execute('''UPDATE classes SET name = %s,description=%s where id=%s''',[name,description,idClass])

def getListClassesNotInTime(timeStart,timeEnd):
    #example : "2022-05-27 03:14:07" and "2022-05-27 05:14:07"
    sql = """ 
    select * from classes where id not in (SELECT distinct(idClasses) FROM lesson where timeStart between %s and %s or
    timeEnd between %s and %s)
    """
    cursor.execute(sql,[timeStart,timeEnd,timeStart,timeEnd])
    rows = cursor.fetchall()
    return rows