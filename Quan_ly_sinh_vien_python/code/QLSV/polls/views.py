import datetime
import json
from tkinter.messagebox import NO
import bcrypt
from django.http import HttpResponse
from django.shortcuts import render
from polls.dto.listDTO import ObjectDTO, ObjectDTOEncoder

from polls.models import Classes, Lesson, Student, Subject, Teacher, User
from polls.service.ClassesService import editClasses, getListClasses, getListClassesNotInTime
from polls.service.LessonService import addNewLesson, countNumberStudentByIdLesson, getInforLesson, getListLessonOnTimeOfTeacher, getListStudentOfLession, getListSubject
from polls.service.UserService import editStudent, editTeacher, editUser, getListStudent, getListTeacher, getListTeacherNotInTime, registerStudent, registerTeacher



def index(request):
    userinfo  = request.session.get('userinfo')
    time = datetime.datetime.today().strftime('%Y/%m/%d')
    if(userinfo) :
        idUser = userinfo[2]
        print(idUser)
        print(time)
        listLessonOnTimeOfTeacher = getListLessonOnTimeOfTeacher(idUser,None,time)
        return render(request,"user/index.html",{"listLessonOnTimeOfTeacher":listLessonOnTimeOfTeacher})
    else :
        return render(request,"others/login.html")

def indexAdmin(request):
    return render(request,"admin/index.html")

def studentManagementView(request):
    listStudent = getListStudent(None)
    return render(request,"admin/student.html",{"listStudent":listStudent})


def searchStudent(request) :
    if request.method == 'POST':
        key=request.POST['table_search_student']
        userinfo  = request.session.get('userinfo')
        if(userinfo) :
            listStudent = getListStudent(key)
            return render(request,"admin/student.html",{"listStudent":listStudent})
        else :
            return render(request,"others/login.html")


def classesManagementView(request):
    listClasses = getListClasses(None)
    return render(request,"admin/lesson.html",{"listClasses":listClasses})

def searchClasses(request) :
    if request.method == 'POST':
        key=request.POST['table_search_classes']
        userinfo  = request.session.get('userinfo')
        if(userinfo) :
            listClasses = getListClasses(key)
            return render(request,"admin/lesson.html",{"listClasses":listClasses})
        else :
            return render(request,"others/login.html")

def teacherManagementView(request):
    listTeacher = getListTeacher(None)
    return render(request,"admin/teacher.html",{"listTeacher":listTeacher})

def searchTeacher(request) :
    if request.method == 'POST':
        key=request.POST['table_search_teacher']
        userinfo  = request.session.get('userinfo')
        if(userinfo) :
            listTeacher = getListTeacher(key)
            return render(request,"admin/teacher.html",{"listTeacher":listTeacher})
        else :
            return render(request,"others/login.html")

def lessonManagementView(request):
    return render(request,"admin/lesson.html")

def login(request):
    return render(request,"others/login.html")


def logout(request):
    userinfo  = request.session.get('userinfo')
    if(userinfo) :
        del request.session['userinfo']
        return render(request,"others/login.html")
    return render(request,"others/login.html")


def search(request) :
    if request.method == 'POST':
        key=request.POST['key']
        userinfo  = request.session.get('userinfo')
        time = datetime.datetime.today().strftime('%d/%m/%Y')
        if(userinfo) :
            idUser = userinfo[2]
            listLessonOnTimeOfTeacher = getListLessonOnTimeOfTeacher(idUser,key,time)
            return render(request,"user/index.html",{"listLessonOnTimeOfTeacher":listLessonOnTimeOfTeacher})
        else :
            return render(request,"others/login.html")


def detailLesson(request,id) :
    userinfo  = request.session.get('userinfo')
    if(userinfo) :
        infoLesson = getInforLesson(id)
        numberStudentOfLession = countNumberStudentByIdLesson(id)
        listStudentOfLession= getListStudentOfLession(id)
        return render(request,"user/detailLesson.html",{"infoLesson":infoLesson,'numberStudentOfLession': numberStudentOfLession,"listStudentOfLession":listStudentOfLession})
    return render(request,"others/login.html")

def addLesson(request):
    listStudent = getListStudent(None)
    listSubject = getListSubject()
    return render(request,"admin/addLessonView.html",{"listStudent":listStudent,"listSubject":listSubject})




#api
def loginApi(request) :
    if request.method == "GET":
        return render(request,"others/login.html")
    else:
        password = request.POST['password']
        email = request.POST['email']
        print(password)
       # hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(14))
        user_login = User.objects.filter(email=email)
        if(user_login) :
            password_db = user_login[0].password[2:len(user_login[0].password)-1]
            if bcrypt.checkpw(password.encode('utf-8') ,password_db.encode('utf-8')):
                userinfo = []
                userinfo.append(user_login[0].fullname)
                userinfo.append(user_login[0].image)
                userinfo.append(user_login[0].id)
                userinfo.append(user_login[0].role)
                if (user_login[0].role=="TEACHER"):
                    teacher_login = Teacher.objects.filter(iduser=user_login[0].id)
                    userinfo.append(teacher_login[0].id)
                request.session['userinfo'] = userinfo
                return  HttpResponse(json.dumps(userinfo), content_type="application/json") 
            else :  return  HttpResponse("500", content_type="application/json") 
        return  HttpResponse("500", content_type="application/json")



def registerStudentApi(request):
    if request.method == "GET":
        return render(request,"home/login.html")
    else:
        username = request.POST['username']
        fullname = request.POST['fullname']
        password = request.POST['password']
        email = request.POST['email']
        image = request.POST['image']
        phone = request.POST['phone']
        address = request.POST['address']
        codeStudent = request.POST['codeStudent']
        image_ = ""
        hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        if(image == None):
            image_='user/img/authors/2.jpg'
            
        else:
            image_ = "user/img/authors/"+image
        user = User(username=username,password=hashed,email=email,fullname=fullname,image=image_,phone=phone,address=address,role="USER")
        registerStudent(user,codeStudent)
        return  HttpResponse("200", content_type="application/json")

def registerClassesApi(request):
    if request.method == "GET":
        return render(request,"home/login.html")
    else:
        name = request.POST['name']
        description = request.POST['description']
        classes = Classes(name=name,description=description)
        classes.save()
        return  HttpResponse("200", content_type="application/json")

#registerTeacherApi 
def registerTeacherApi(request):
    if request.method == "GET":
        return render(request,"home/login.html")
    else:
        username = request.POST['username']
        fullname = request.POST['fullname']
        password = request.POST['password']
        email = request.POST['email']
        image = request.POST['image']
        phone = request.POST['phone']
        address = request.POST['address']
        codeTeacher = request.POST['codeTeacher']
        image_ = ""
        hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        if(image == None):
            image_='user/img/authors/2.jpg'
            
        else:
            image_ = "user/img/authors/"+image
        user = User(username=username,password=hashed,email=email,fullname=fullname,image=image_,phone=phone,address=address,role="TEACHER")
        registerTeacher(user,codeTeacher)
        return  HttpResponse("200", content_type="application/json") 

def editStudentApi(request):
    if request.method == "GET":
        return render(request,"others/login.html")
    else:
        username = request.POST['username']
        fullname = request.POST['fullname']
        # password = request.POST['password_edit']
        email = request.POST['email']
        image = request.POST['image']
        phone = request.POST['phone']
        address = request.POST['address']
        codeStudent = request.POST['codeStudent']
        idUser = request.POST['idUser']
        idStudent = request.POST['idStudent']
        image_ = ""
       
        # hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        if(image == None ):
            editUser(idUser,username,fullname,phone,email,address,None)
        else:
            image_ = "user/img/authors/"+image
            editUser(idUser,username,fullname,phone,email,address,image_)

        editStudent(idStudent,codeStudent)
        return  HttpResponse("200", content_type="application/json") 


def editTeacherApi(request):
    if request.method == "GET":
        return render(request,"others/login.html")
    else:
        username = request.POST['username']
        fullname = request.POST['fullname']
        # password = request.POST['password_edit']
        email = request.POST['email']
        image = request.POST['image']
        phone = request.POST['phone']
        address = request.POST['address']
        codeTeacher = request.POST['codeTeacher']
        idUser = request.POST['idUser']
        idTeacher = request.POST['idTeacher']
        image_ = ""
       
        # hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        if(image == None ):
            editUser(idUser,username,fullname,phone,email,address,None)
        else:
            image_ = "user/img/authors/"+image
            editUser(idUser,username,fullname,phone,email,address,image_)

        editTeacher(idTeacher,codeTeacher)
        return  HttpResponse("200", content_type="application/json") 


def editClassesApi(request):
    if request.method == "GET":
        return render(request,"others/login.html")
    else:
        name = request.POST['name']
        description = request.POST['description']
        idClass = request.POST['idClass']
        editClasses(idClass,name,description)
        return  HttpResponse("200", content_type="application/json")


def uploadFileApi(request):
    if request.method == "GET":
        return render(request,"others/login.html")
    else:
        file_obj = request.FILES.get('file') 
        # print("The name of the uploaded file is:", file_obj.name)
        # print("The size of the uploaded file is:", file_obj.size)
        f = open('polls/static/user/img/authors/' + file_obj.name + "", 'wb')    
        for line in file_obj.chunks():                    
            f.write(line)                                  
        f.close()
        url = '/static/user/img/authors/'+file_obj.name
        return HttpResponse(url)


def detailStudentApi(request) :
    idUser = request.GET['idUser']
    idStudent = request.GET['idStudent']
    user = User.objects.filter(id=idUser)
    student = Student.objects.filter(id=idStudent)
    userinfo = []
    userinfo.append(user[0].username) #0
    userinfo.append(user[0].fullname) #1
    # userinfo.append(user[0].password)
    userinfo.append(user[0].email) #2
    userinfo.append(user[0].image) #3
    userinfo.append(user[0].phone) #4
    userinfo.append(user[0].address) #5
    userinfo.append(student[0].codestudent) #6
    userinfo.append(idStudent)
    userinfo.append(idUser)
    return  HttpResponse(json.dumps(userinfo), content_type="application/json") 

def detailTeacherApi(request) :
    idUser = request.GET['idUser']
    idTeacher = request.GET['idTeacher']
    user = User.objects.filter(id=idUser)
    teacher = Teacher.objects.filter(id=idTeacher)
    userinfo = []
    userinfo.append(user[0].username) #0
    userinfo.append(user[0].fullname) #1
    # userinfo.append(user[0].password)
    userinfo.append(user[0].email) #2
    userinfo.append(user[0].image) #3
    userinfo.append(user[0].phone) #4
    userinfo.append(user[0].address) #5
    userinfo.append(teacher[0].codeteacher) #6
    userinfo.append(idTeacher)
    userinfo.append(idUser)
    return  HttpResponse(json.dumps(userinfo), content_type="application/json") 


def detailClassesApi(request) :
    idClass = request.GET['idClass']
    classes = Classes.objects.filter(id=idClass)
    classInfor = []
    classInfor.append(classes[0].name) #0
    classInfor.append(classes[0].description) #1
    classInfor.append(idClass) #1
    # userinfo.append(user[0].password)
    return  HttpResponse(json.dumps(classInfor), content_type="application/json") 

def filterLessonByDateApi(request) :
    dateFilter = request.GET['date']
    userinfo  = request.session.get('userinfo')
    if(userinfo) :
        idUser = userinfo[2]
        listLessonOnTimeOfTeacher = getListLessonOnTimeOfTeacher(idUser,None,dateFilter)
        return  HttpResponse(json.dumps(listLessonOnTimeOfTeacher,default=str), content_type="application/json") 
    else :
        return render(request,"others/login.html")


def addNewLessonApi(request):
    if request.method == "GET":
        return render(request,"others/login.html")
    else:
        # try:
        #     idClasses = request.POST['classes']
        #     idTeacher = request.POST['teacher']
        #     idSubject = request.POST['subject']
        #     timeStart = request.POST['timeStart']
        #     timeEnd = request.POST['timeEnd']
        #     listIdStudent = request.POST['listIdStudent']
        #     lesson = Lesson(idclasses=idClasses,idteacher=idTeacher,idsubject=idSubject,timestart=timeStart,timeend=timeEnd,description="Thêm mới tiết học thành công!")
        #     addNewLesson(lesson,listIdStudent)
        #     return  HttpResponse("200", content_type="application/json")
        # except:
        #     return  HttpResponse("500", content_type="application/json")
        idClasses = request.POST['classes']
        idTeacher = request.POST['teacher']
        idSubject = request.POST['subject']
        timeStart = request.POST['timeStart']
        timeEnd = request.POST['timeEnd']
        listIdStudent = request.POST['listIdStudent']
        classes = Classes.objects.get(id=idClasses)
        teacher = Teacher.objects.get(id=idTeacher)
        subject = Subject.objects.get(id=idSubject)
        lesson = Lesson(idclasses=classes,idteacher=teacher,idsubject=subject,timestart=timeStart,timeend=timeEnd,description="Thêm mới tiết học thành công!")
        addNewLesson(lesson,listIdStudent.split(","))
        return  HttpResponse("200", content_type="application/json")

def getIdTeacherAndIdClassByDateApi(request):
    try:
        # example "2022-05-27 03:14:07" and "2022-05-27 05:14:07"
        timeStart = request.GET['timeStart']
        timeEnd = request.GET['timeEnd']
        # listClass = getListClassesNotInTime("2022-05-27 03:14:07","2022-05-27 05:14:07")
        # listTeacher = getListTeacherNotInTime("2022-05-27 03:14:07","2022-05-27 05:14:07")
        listClass = getListClassesNotInTime(timeStart,timeEnd)
        listTeacher = getListTeacherNotInTime(timeStart,timeEnd)
        objectDto = ObjectDTO(listTeacher,listClass)
        print(listClass)
        print(listTeacher)
        return  HttpResponse(json.dumps(objectDto,cls=ObjectDTOEncoder), content_type="application/json") 
    except:
        return  HttpResponse("500", content_type="application/json")


##############################################

