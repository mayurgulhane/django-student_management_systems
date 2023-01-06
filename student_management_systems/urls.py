"""student_management_systems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views, Hod_Views, Teacher_Views, Student_Views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login Path
    path('',views.LogIn,name='LogIn'),
    path('doLogin',views.doLogIn,name='doLogIn'),
    path('doLogout',views.doLogOut,name='doLogOut'),

    # Profile
    path('hod/profile',views.userProfile,name="userProfile"),
    path('hod/profile/update',views.profileUpdate,name="profileUpdate"),

    # HOD Panel
    path('hod/home',Hod_Views.hodHome,name='hodHome'),

    # Course
    path('hod/course/add',Hod_Views.courseAdd,name='courseAdd'),
    path('hod/course/list',Hod_Views.courseList,name='courseList'),
    path('hod/course/edit/<str:id>',Hod_Views.courseEdit,name='courseEdit'),
    path('hod/course/update',Hod_Views.courseUpdate,name='courseUpdate'),
    path('hod/course/delete/<str:id>',Hod_Views.courseDelete,name='courseDelete'),

    # Session
    path('hod/session/add',Hod_Views.sessionAdd, name='sessionAdd'),
    path('hod/session/list',Hod_Views.sessionList, name='sessionList'),
    path('hod/session/edit/<str:id>',Hod_Views.sessionEdit, name='sessionEdit'),
    path('hod/session/update',Hod_Views.sessionUpdate, name='sessionUpdate'),
    path('hod/session/delete/<str:id>',Hod_Views.sessionDelete, name='sessionDelete'),

    # Student
    path('hod/student/add',Hod_Views.studentAdd, name='studentAdd'),
    path('hod/student/list',Hod_Views.studentList, name='studentList'),
    path('hod/student/edit/<str:id>',Hod_Views.studentEdit, name='studentEdit'),
    path('hod/student/update',Hod_Views.studentUpdate, name='studentUpdate'),
    path('hod/student/delete/<str:id>',Hod_Views.studentDelete, name='studentDelete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
