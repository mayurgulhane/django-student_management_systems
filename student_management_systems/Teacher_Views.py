from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from app.models import Teacher,Teacher_Notification,Teacher_Leave, Teacher_Feedback, Subject, Session_Year, Student, Attendance,Attendance_Report, Student_Result


@login_required(login_url='/')
def teacherHome(request):
    teacherName = Teacher.objects.get(admin=request.user.id)

    getSubjectCount = Subject.objects.filter(teacher_name=teacherName).count()
    print(getSubjectCount)


    getStudentCount = Student.objects.filter(course_id=getSubjectCount).count()
    print(getStudentCount)

    applyLeave = Teacher_Leave.objects.filter(teacher_id=teacherName.id)
    print(applyLeave)
    
    applyLeaveCount=0
    for i in applyLeave:
        if i.status == 1:
            applyLeaveCount = applyLeaveCount+1
    print(applyLeaveCount)

    notifi = Teacher_Notification.objects.filter(teacher_id = teacherName.id)

    seenCount = 0
    for i in notifi:
        if i.status == 1:
            seenCount = seenCount + 1
    print(seenCount)

    context = {
        'getSubjectCount' : getSubjectCount,
        'getStudentCount' : getStudentCount,
        'applyLeave' : applyLeave,
        'applyLeaveCount' : applyLeaveCount,
        'notifi' : notifi,
        'seenCount' : seenCount
    }

    return render(request,'Teacher/Home.html',context)


# ======================= NOTIFICATION START ====================

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

# ================== NOTIFICATION END =========================


# ================ APPLY LEAVE APPLICATION START ===============

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

# ================= APPLY LEAVE APPLICATION END ==================


# ==================== FEEDBACK START =======================

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

        messages.success(request,'Feedback Sucessfully Send..')
        return redirect('teacherFeedback')

    context ={
        'feedback' : feedback
    }
    return render(request,'Teacher/feedback.html',context)

# ===================== FEEDBACK END =====================


# ==================== TAKE ATTENDANCE START ============

@login_required(login_url='/')
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


@login_required(login_url='/')
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

        messages.success(request,'Saved Attendance')
        return redirect('takeAttendanceTeacher')

# =================== TAKE ATTENDANCE END ===================


# ================= VIEW ATTENDANCE START ===================

@login_required(login_url='/')
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

# ====================== VIEW ATTENDANCE END ==============


# ================== RESULT START =============================

@login_required(login_url='/')
def addResult(request):
    teacherId = Teacher.objects.get(admin = request.user.id)
      
    teacherSubject = Subject.objects.filter(teacher_name=teacherId)
    sessionYear = Session_Year.objects.all()
    print(teacherSubject,'j')

    action = request.GET.get('action')

    getsubject = None
    getsession = None
    studentList = None

    if action is not None:
        if request.method == "POST":
            subjectId = request.POST['subject_id']
            sessionId = request.POST['session_id']

            getsubject = Subject.objects.get(id=subjectId)
            getsession = Session_Year.objects.get(id=sessionId)
            
          
            student_id = getsubject.course_name.id # 3
            studentList=Student.objects.filter(course_id=student_id)
            print(studentList)

    context = {
        'teacherSubject' : teacherSubject,
        'sessionYear' : sessionYear,
        'action' : action,
        'getsubject' : getsubject,
        'getsession' : getsession,
        'studentList' : studentList
    }

    return render(request,'Teacher/add_result.html',context)


@login_required(login_url='/')
def saveResult(request):
    if request.method == "POST":
        studentId = request.POST['student_id']
        subjectId = request.POST['subject_id']
        sessionId = request.POST['session_id']
        assignmentMark = request.POST['assignment_mark']
        examMark = request.POST['exam_mark']

        getStudent = Student.objects.get(id=studentId)
        getSubject = Subject.objects.get(id=subjectId)

        checkExists = Student_Result.objects.filter(student_id = getStudent,subject_id=getSubject).exists()
        print(checkExists)
        
        if checkExists:
            result = Student_Result.objects.get(student_id=getStudent, subject_id=getSubject)
            result.assignment_mark = assignmentMark
            result.exam_mark = examMark
            result.save()

            messages.success(request,'Results are Successfully Updated..')
            return redirect('addResult')

        else:
            result = Student_Result(
                student_id = getStudent,
                subject_id = getSubject,
                assignment_mark = assignmentMark,
                exam_mark = examMark
            )
            result.save()
            
            messages.success(request,'Results are Successfully Added..')
            return redirect('addResult')

    return render(request,'Teacher/add_result.html')

# ====================  RESULT END ============================