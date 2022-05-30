from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin', views.indexAdmin, name='indexAdmin'),
    path('login', views.login, name='login'),
    path('search', views.search, name='search'),  
    path('logout', views.logout, name='logout'),
    path('lesson/<int:id>', views.detailLesson, name='detailLesson'),
    path('student', views.studentManagementView, name='studentManagementView'),  
    path('teacher', views.teacherManagementView, name='teacherManagementView'),
    path('lesson', views.classesManagementView, name='classesManagementView'), 
    path('searchStudent', views.searchStudent, name='searchStudent'), 
    path('searchTeacher', views.searchTeacher, name='searchTeacher'), 
    path('searchClasses', views.searchClasses, name='searchClasses'), 
    path('addLesson', views.addLesson, name='addLesson'), 






    path('loginApi', views.loginApi, name='loginApi'),
    path('registerStudentApi', views.registerStudentApi, name='registerStudentApi'),
    path('registerTeacherApi', views.registerTeacherApi, name='registerTeacherApi'),
    path('registerClassesApi', views.registerClassesApi, name='registerClassesApi'),
    path('uploadFileApi', views.uploadFileApi, name='uploadFileApi'),
    path('detailStudentApi', views.detailStudentApi, name='detailStudentApi'),
    path('detailTeacherApi', views.detailTeacherApi, name='detailTeacherApi'),
    path('detailClassesApi', views.detailClassesApi, name='detailClassesApi'),
    path('editStudentApi', views.editStudentApi, name='editStudentApi'),
    path('editTeacherApi', views.editTeacherApi, name='editTeacherApi'),
    path('editClassesApi', views.editClassesApi, name='editClassesApi'),
    path('filterLessonByDateApi', views.filterLessonByDateApi, name='filterLessonByDateApi'),
    path('getIdTeacherAndIdClassByDateApi', views.getIdTeacherAndIdClassByDateApi, name='getIdTeacherAndIdClassByDateApi'),
    path('addNewLessonApi', views.addNewLessonApi, name='addNewLessonApi'),

]