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
