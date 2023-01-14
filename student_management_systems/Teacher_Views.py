from django.shortcuts import render, redirect
from app.models import Teacher,Teacher_Notification,Teacher_Leave, Teacher_Feedback, Subject, Session_Year, Student, Attendance,Attendance_Report
from django.contrib import messages
from django.contrib.auth.decorators import login_required 


@login_required(login_url='/')
def teacherHome(request):
    return render(request,'Teacher/Home.html')


# =============================== NOTIFICATION START ==================================

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

# ======================= NOTIFICATION END ====================================


# ================ APPLY LEAVE APPLICATION START ================================

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
        return redirect('applyLeaveTeacher')

# ====================== APPLY LEAVE APPLICATION END =============================


# ======================= FEEDBACK START ==========================================

@login_required(login_url='/')
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

# =========================== FEEDBACK END ===========================================


# =========================== TAKE ATTENDANCE START ====================================

def takeAttendance(request):
    teacher_name = Teacher.objects.get(admin=request.user.id) # Teacher full name Parnav Kawade

    subjectName = Subject.objects.filter(teacher_name = teacher_name)
    sessionYear = Session_Year.objects.all()

    action = request.GET.get('action')

    getSubject = None
    getSession = None
    students = None

    if action is not None:
        if request.method == "POST":
            subjectId = request.POST['subject_id'] # id 1
            sessionId = request.POST['session_id']

            getSubject = Subject.objects.get(id=subjectId) # Subject name- Python
            getSession = Session_Year.objects.get(id=sessionId)


            student_id = getSubject.course_name.id # 3
            students = Student.objects.filter(course_id = student_id) # students Model

    context ={
        'subjectName' : subjectName,
        'sessionYear' : sessionYear,
        'getSubject' : getSubject,
        'getSession' : getSession,
        'action' : action,
        'students' : students
    }

    return render(request,'Teacher/take_attendance.html',context)


def saveAttendanceTeacher(request):
    if request.method == "POST":
        subjectId = request.POST['subject_id']
        sessionId = request.POST['session_id']
        attendanceDate = request.POST['attendance_date']
        attendanceStudents = request.POST.getlist('attendance_student')

        subjectName = Subject.objects.get(id=subjectId) #subject name - Os
        sessionYear = Session_Year.objects.get(id=sessionId)

        attendance = Attendance(
            subject_id = subjectName,
            attendance_date = attendanceDate,
            session_year_id = sessionYear
         )
        attendance.save()

        for i in attendanceStudents:
            presentStudent = Student.objects.get(id=i)

            attendanceReport = Attendance_Report(
                student_id = presentStudent,
                attendance_id = attendance,
            )
            attendanceReport.save()

        print(subjectId,sessionId,attendanceDate,attendanceStudents)
        return redirect('takeAttendanceTeacher')

# =========================== TAKE ATTENDANCE END ====================================


# =========================== VIEW ATTENDANCE START ====================================

def viewAttendance(request):
    action = request.GET.get('action')

    teacherName = Teacher.objects.get(admin=request.user.id)

    subjectName = Subject.objects.filter(teacher_name=teacherName)
    sessionYear = Session_Year.objects.all()

    getSubject = None
    getsession = None
    attendanceDate = None
    presentStudent = None

    if action is not None:
        if request.method == "POST":
            subjectId = request.POST['subject_id']
            sessionId = request.POST['session_id']
            attendanceDate = request.POST['attendance_date']

            getSubject = Subject.objects.get(id=subjectId)
            getsession = Session_Year.objects.get(id=sessionId)

            
            attendance= Attendance.objects.filter(
                subject_id=getSubject,
                attendance_date=attendanceDate
            )

            for i in attendance:
                presentStudent = Attendance_Report.objects.filter(attendance_id=i)
                print(presentStudent)

    context ={
        'subjectName' : subjectName,
        'sessionYear' : sessionYear,
        'getSubject' : getSubject,
        'getsession' : getsession,
        'action' : action,
        'attendanceDate' : attendanceDate,
        'presentStudent' : presentStudent
    }

    return render(request,'Teacher/view_attendance.html',context)

# =========================== VIEW ATTENDANCE END ====================================

