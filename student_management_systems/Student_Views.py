from django.shortcuts import render, redirect
from app.models import Student, Student_Notification, Student_Feedback, Student_Leave
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def stuentHome(request):
    return render(request, 'student/Home.html')

# ============================ Notification Start ================================

@login_required(login_url='/')
def notification(request):
    studentId = Student.objects.get(admin=request.user.id)

    receiveNotification = Student_Notification.objects.filter(student_id=studentId)

    context = {
        'receiveNotification': receiveNotification
    }

    return render(request, 'student/notification.html', context)

@login_required(login_url='/')
def seenNotification(request, status):
    notify = Student_Notification.objects.get(id=status)
    notify.status = 1
    notify.save()

    return redirect('notification')

# ============================== Notification End ================================


# ============================ FEEDBACK START ================================

@login_required(login_url='/')
def studentFeedback(request):
    studentName = Student.objects.get(admin=request.user.id)

    feedback = Student_Feedback.objects.filter(student_id=studentName.id)
    print(feedback)

    if request.method == "POST":
        feedback = request.POST['feedback_message']

        studentFeedback = Student_Feedback(
            student_id = studentName,
            feedback = feedback
        )
        studentFeedback.save()
        return redirect('studentFeedback')

    context = {
        'feedback' : feedback
    }

    return render(request,'Student/feedback.html',context)

# ============================== FEEDBACK END ===================================


# ============================ APPLY LEAVE START ================================

@login_required(login_url='/')
def applyLeave(request):
    studentName = Student.objects.get(admin=request.user.id)

    applyLeaveHistory = Student_Leave.objects.filter(student_id=studentName.id)
    print(applyLeaveHistory)

    context ={
        'applyLeaveHistory' : applyLeaveHistory
    }

    return render(request,'Student/apply_leave.html',context)

@login_required(login_url='/')
def sendApplyLeave(request):
    if request.method == "POST":
        leaveDate = request.POST['leave_date']
        leaveMessage = request.POST['leave_message']

        studentName = Student.objects.get(admin=request.user.id)

        applyLeave = Student_Leave(
            student_id = studentName,
            data = leaveDate,
            message = leaveMessage
        )
        applyLeave.save()

        return redirect('applyLeave')
    return render(request,'Student/apply_leave.html')

# ============================== APPLY LEAVE END ===================================