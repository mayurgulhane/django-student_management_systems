from django.shortcuts import render, redirect
from app.models import Teacher,Teacher_Notification

def Home(request):
    return render(request,'Teacher/Home.html')


# ================ Notification Start ================================


def notifications(request):
    teacherId = Teacher.objects.get(admin = request.user.id)
    print(teacherId)
    print(teacherId.id)

    notifi = Teacher_Notification.objects.filter(teacher_id = teacherId.id)

    context = {
        'notifi' : notifi
    }

    return render(request,'Teacher/notification.html',context)


def seenNotification(request,status):
    notifi = Teacher_Notification.objects.get(id=status)
    notifi.status = 1
    notifi.save()
    return redirect('notifications')

# ================ Notification End ================================
