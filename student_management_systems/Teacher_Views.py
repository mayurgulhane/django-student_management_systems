from django.shortcuts import render, redirect
from app.models import Teacher,Teacher_Notification,Teacher_Leave, Teacher_Feedback
from django.contrib import messages
from django.contrib.auth.decorators import login_required 


@login_required(login_url='/')
def teacherHome(request):
    return render(request,'Teacher/Home.html')


# ================ Notification Start ================================

@login_required(login_url='/')
def notifications(request):
    teacherName = Teacher.objects.get(admin = request.user.id)
    print(teacherName)
    print(teacherName.id)

    notifi = Teacher_Notification.objects.filter(teacher_id = teacherName.id)

    context = {
        'notifi' : notifi
    }

    return render(request,'Teacher/notification.html',context)


@login_required(login_url='/')
def seenNotification(request,status):
    notifi = Teacher_Notification.objects.get(id=status)
    notifi.status = 1
    notifi.save()
    return redirect('notifications')

# ================ Notification End ================================


# ================ Leave Application Start ================================

@login_required(login_url='/')
def applyLeave(request):
    teacherName = Teacher.objects.get(admin=request.user.id)
    print(teacherName)

    applyLeaveHistory = Teacher_Leave.objects.filter(teacher_id=teacherName.id)

    context = {
        'applyLeaveHistory' : applyLeaveHistory
    }

    return render(request,'Teacher/apply_leave.html',context)

@login_required(login_url='/')
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

def teacherFeedback(request):
    teacherName = Teacher.objects.get(admin=request.user.id)

    feedback = Teacher_Feedback.objects.filter(teacher_id = teacherName.id)

    if request.method == "POST":
        
        feedbackMessage = request.POST['feedback_message']

        teacherFeedback = Teacher_Feedback(
            teacher_id = teacherName,
            feedback = feedbackMessage,
            reply_feedback = ""
        )
        teacherFeedback.save()
        return redirect('teacherFeedback')

    
    context ={
        'feedback' : feedback
    }
    return render(request,'Teacher/feedback.html',context)