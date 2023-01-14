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

#==================================== HOD Panel ======================================

    # HOD Home
    path('hod/home',Hod_Views.hodHome,name='hodHome'),

    # Courses
    path('hod/course/add',Hod_Views.courseAdd,name='courseAdd'),
    path('hod/course/list',Hod_Views.courseList,name='courseList'),
    path('hod/course/edit/<str:id>',Hod_Views.courseEdit,name='courseEdit'),
    path('hod/course/update',Hod_Views.courseUpdate,name='courseUpdate'),
    path('hod/course/delete/<str:id>',Hod_Views.courseDelete,name='courseDelete'),

    # Sessions
    path('hod/session/add',Hod_Views.sessionAdd, name='sessionAdd'),
    path('hod/session/list',Hod_Views.sessionList, name='sessionList'),
    path('hod/session/edit/<str:id>',Hod_Views.sessionEdit, name='sessionEdit'),
    path('hod/session/update',Hod_Views.sessionUpdate, name='sessionUpdate'),
    path('hod/session/delete/<str:id>',Hod_Views.sessionDelete, name='sessionDelete'),

    # Students
    path('hod/student/add',Hod_Views.studentAdd, name='studentAdd'),
    path('hod/student/list',Hod_Views.studentList, name='studentList'),
    path('hod/student/edit/<str:id>',Hod_Views.studentEdit, name='studentEdit'),
    path('hod/student/update',Hod_Views.studentUpdate, name='studentUpdate'),
    path('hod/student/delete/<str:id>',Hod_Views.studentDelete, name='studentDelete'),

    # Teachers
    path('hod/teacher/add',Hod_Views.teacherAdd, name='teacherAdd'),
    path('hod/teacher/list',Hod_Views.teacherList, name='teacherList'),
    path('hod/teacher/edit/<str:id>',Hod_Views.teacherEdit, name='teacherEdit'),
    path('hod/teacher/update',Hod_Views.teacherUpdate, name='teacherUpdate'),
    path('hod/teacher/delete/<str:id>',Hod_Views.teacherDelete, name='teacherDelete'),

    # Subjects
    path('hod/subject/add',Hod_Views.subjectAdd, name='subjectAdd'),
    path('hod/subject/list',Hod_Views.subjectList, name='subjectList'),
    path('hod/subject/edit/<str:id>',Hod_Views.subjectEdit, name='subjectEdit'),
    path('hod/subject/update',Hod_Views.subjectUpdate, name='subjectUpdate'),
    path('hod/subject/delete/<str:id>',Hod_Views.subjectDelete, name='subjectDelete'),

    # Notifications send to TEACHER
    path('hod/teacher_notification',Hod_Views.teacherNotification,name='teacherNotification'),
    path('hod/save_teacher_notification',Hod_Views.saveTeacherNotification,name='saveTeacherNotification'),

    # Notifications send to STUDENT
    path('hod/student/notification',Hod_Views.studentNotification,name='studentNotification'),

    # Hod receive to TEACHER Leave
    path('hod/teacher_leave',Hod_Views.teacherLeave,name='teacherLeave'),

    path('hod/teacher_leave_approve/<str:id>',Hod_Views.approveTeacherLeave,name='approveTeacherLeave'),
    path('hod/teacher_leave_disapprove/<str:id>',Hod_Views.disapproveTeacherLeave,name='disapproveTeacherLeave'),

    # Hod receive to STUDENT Leave
    path('hod/student_leave',Hod_Views.studentLeave,name='studentLeave'),

    path('hod/student_leave_approve/<str:id>',Hod_Views.approveStudentLeave,name='approveStudentLeave'),
    path('hod/student_leave_disapprove/<str:id>',Hod_Views.disapproveStudentLeave,name='disapproveStudentLeave'),

    # Hod receive to TEACHER Feedback
    path('hod/teacher/feedback',Hod_Views.teacherFeedbackReceive,name='teacherFeedbackReceive'),
    path('hod/teacher/feedback_reply',Hod_Views.teacherFeedbackSend,name='teacherFeedbackSend'),

    # Hod receive to STUDENT Feedback
    path('hod/student/feedback',Hod_Views.studentFeedbackReceive, name='studentFeedbackReceive'),
    path('hod/student/feedback_reply',Hod_Views.studentFeedbackSend, name='studentFeedbackSend'),

    # Teachers View Attendance
    path('hod/student/view_attendance',Hod_Views.viewAttendance, name='viewAttendance'),


#==================================== Teachers Panel ======================================

    # Teachers Home
    path('teacher/home', Teacher_Views.teacherHome, name='teacherHome'),

    # Teachers Notification
    path('teacher/notification', Teacher_Views.notifications, name='notifications'),
    path('teacher/seen_notification/<str:status>', Teacher_Views.seenNotification, name='seenNotification'),

    # Teachers Apply Leave
    path('teacher/apply_leave',Teacher_Views.applyLeave,name='applyLeaveTeacher'),
    path('teacher/save_apply_leave',Teacher_Views.saveApplyLeave,name='saveApplyLeave'),

    # Teachers Feedback
    path('teacher/feedback',Teacher_Views.teacherFeedback,name='teacherFeedback'),


    # Teachers Take Attendance
    path('teacher/take_attendance', Teacher_Views.takeAttendance, name='takeAttendanceTeacher'),
    path('teacher/save_attendance', Teacher_Views.saveAttendanceTeacher, name='saveAttendanceTeacher'),

    # Teachers View Attendance
    path('teacher/view_attendance',Teacher_Views.viewAttendance, name='viewAttendanceTeacher'),

#==================================== Student Panel ======================================

    path('student/home',Student_Views.stuentHome,name='stuentHome'),

    # Student Notification
    path('student/notification',Student_Views.notification,name='notification'),
    path('student/seen_notification/<str:status>', Student_Views.seenNotification,name='seenNotification'),

    # Student Feedback
    path('student/feedback', Student_Views.studentFeedback, name='studentFeedback'),

     # Student Apply Leave
    path('student/apply_leave',Student_Views.applyLeave,name='applyLeave'),
    path('student/send_apply_leave',Student_Views.sendApplyLeave,name='sendApplyLeave'),

    # Student View Attendance
    path('student/view_attendance',Student_Views.viewAttendance, name='viewAttendanceStudent'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
