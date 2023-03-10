from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class UserModel(UserAdmin):
    list_display = ['username','user_type']

admin.site.register(CustomUser,UserModel)
admin.site.register((Course,Session_Year,Student,Teacher,Subject))
admin.site.register((Teacher_Notification,Teacher_Leave,Teacher_Feedback))
admin.site.register((Student_Notification, Student_Feedback, Student_Leave))
admin.site.register((Attendance, Attendance_Report,Student_Result))
