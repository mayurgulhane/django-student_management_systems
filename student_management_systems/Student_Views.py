from django.shortcuts import render, redirect
from app.models import Student, Student_Notification


def stuentHome(request):
    return render(request, 'student/Home.html')

# ============================ Notification Start ================================

def notification(request):
    studentId = Student.objects.get(admin=request.user.id)

    receiveNotification = Student_Notification.objects.filter(student_id=studentId)

    context = {
        'receiveNotification': receiveNotification
    }
    return render(request, 'student/notification.html', context)


def seenNotification(request, status):
    notify = Student_Notification.objects.get(id=status)
    notify.status = 1
    notify.save()
    return redirect('notification')

# ============================== Notification End ================================