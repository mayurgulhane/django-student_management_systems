from django.shortcuts import render, redirect
from app.models import Teacher,Teacher_Notification,Teacher_Leave
from django.contrib import messages

def Home(request):
    return render(request,'Teacher/Home.html')


# ================ Notification Start ================================


def notifications(request):
    teacherName = Teacher.objects.get(admin = request.user.id)
    print(teacherName)
    print(teacherName.id)

    notifi = Teacher_Notification.objects.filter(teacher_id = teacherName.id)

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


# ================ Leave Application Start ================================


def applyLeave(request):
    teacherName = Teacher.objects.get(admin=request.user.id)
    print(teacherName)

    applyLeaveHistory = Teacher_Leave.objects.filter(teacher_id=teacherName.id)

    context = {
        'applyLeaveHistory' : applyLeaveHistory
    }

    return render(request,'Teacher/apply_leave.html',context)


def saveApplyLeave(request):
    if request.method == "POST":
        leaveDate = request.POST['leave_date']
        leaveMessage = request.POST['leave_message']

        teacherName = Teacher.objects.get(admin=request.user.id)
        print("id : ",teacherName)

        applyLeave = Teacher_Leave(
            teacher_id = teacherName,
            data = leaveDate,
            message = leaveMessage
            )
        applyLeave.save()

        messages.success(request,'Leave Application Sucessfully Send..')
        return redirect('applyLeave')

# ================ Leave Application End ================================