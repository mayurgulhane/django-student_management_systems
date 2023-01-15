from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Student, Student_Notification, Student_Feedback, Student_Leave, Subject, Attendance, Attendance_Report, Student_Result
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def stuentHome(request):
    studentName = Student.objects.get(admin=request.user.id)
    print(studentName.course_id)
    subjectCount = Subject.objects.filter(course_name=studentName.course_id).count()
   
    passed = Student_Result.objects.filter(student_id=studentName)
    print(passed)

    passedCount= 0
    for i in passed:
        total = (i.assignment_mark + i.exam_mark)/2
        if total >= 35:
            passedCount=passedCount+1
    print(passedCount)


    applyLeave = Student_Leave.objects.filter(student_id=studentName.id)
    print(applyLeave)
    
    applyLeaveCount=0
    for i in applyLeave:
        if i.status == 1:
            applyLeaveCount = applyLeaveCount+1
    print(applyLeaveCount)
    
    context ={
        'subjectCount' : subjectCount,
        'studentName' : studentName,
        'passed' : passed,
        'passedCount' : passedCount,
        'applyLeave' : applyLeave,
        'applyLeaveCount' : applyLeaveCount,
        
    }
    return render(request, 'student/Home.html',context)

# ====================== Notification Start =======================

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

# ==================== Notification End ===============


# ================= FEEDBACK START ====================

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

        messages.success(request,'Feedback Sucessfully Send..')
        return redirect('studentFeedback')

    context = {
        'feedback' : feedback
    }

    return render(request,'Student/feedback.html',context)

# =================== FEEDBACK END ==============================


# =================== APPLY LEAVE START =======================

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

        messages.success(request,'Leave Application Sucessfully Send..')

    return render(request,'Student/apply_leave.html')

# ======================= APPLY LEAVE END ===================


# ===================== VIEW ATTENDANCE START =================

@login_required(login_url='/')
def viewAttendance(request):
    studentCourse = Student.objects.get(admin=request.user.id)
    print(studentCourse.course_id) # MSC

    subjects = Subject.objects.filter(course_name = studentCourse.course_id)
    # print(subjects) # <QuerySet [<Subject: Java Core>, <Subject: EDC>]>

    action = request.GET.get('action')

    subjectName = None
    showattendance = None

    if action is not None:
        if request.method == "POST":
            subjectId = request.POST['subject_id']
            print(subjectId)
            subjectName = Subject.objects.get(id=subjectId)

            showattendance = Attendance_Report.objects.filter(student_id=studentCourse,attendance_id__subject_id=subjectId)
            print(showattendance)

    context ={
        'subjects' : subjects,
        'action' : action,
        'subjectName' : subjectName,
        'showattendance' : showattendance
       
    }
    
    return render(request,'Student/view_attendance.html',context)

# ===================== VIEW ATTENDANCE END =================


# ===================== VIEW RESULT START =================

@login_required(login_url='/')
def viewResult(request):
    getStudent = Student.objects.get(admin=request.user.id)
    result = Student_Result.objects.filter(student_id=getStudent)
    print(result)
   
    total = 0
    for i in result:
        assignMark = i.assignment_mark
        examMark = i.exam_mark

        total=(assignMark+examMark)/2
        print(total)

    context ={
        'result' : result,
        'total' : total,
    }

    return render(request,'Student/view_result.html',context)

# ===================== VIEW ATTENDANCE END =================