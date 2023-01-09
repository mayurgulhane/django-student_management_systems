from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Course,Session_Year, CustomUser, Student, Teacher, Subject, Teacher_Notification

@login_required(login_url='/')
def hodHome(request):
    studentsCount = Student.objects.all().count()
    teachersCount = Teacher.objects.all().count()
    coursesCount = Course.objects.all().count()
    subjectsCount = Subject.objects.all().count()

    studentGenderMale = Student.objects.filter(gender="Male").count()
    studentGenderFemale = Student.objects.filter(gender="Female").count()
    print(studentGenderMale)
    print(studentGenderFemale)

    

    context = {
        'studentsCount' : studentsCount,
        'teachersCount' : teachersCount,
        'coursesCount' : coursesCount,
        'subjectsCount' : subjectsCount,
        'studentGenderMale' : studentGenderMale,
        'studentGenderFemale' : studentGenderFemale,
    }

    messages.success(request,"Log In Successfully..")
    return render(request,"Hod/hodHome.html",context)

# =============== COURSE START =========================================

@login_required(login_url='/')
def courseAdd(request):
    if request.method == "POST":
        courseName = request.POST['name']
        duration = request.POST['duration']
        print(courseName,duration)

        course = Course(
            name = courseName,
            duration = duration
        )
        course.save()

        messages.success(request,'Course Are Successfully Added ...')
        request.session["name"] = course.name
        return redirect('courseAdd')

    return render(request,"Hod/course_add.html")


@login_required(login_url='/')
def courseList(request):
    course = Course.objects.all()

    context = {
        'course': course
    }

    return render(request,'Hod/course_list.html',context)


@login_required(login_url='/')
def courseEdit(request,id):
    course = Course.objects.get(id = id)

    context = {
        'course':course
    }

    return render(request,'Hod/course_edit.html',context)


@login_required(login_url='/')
def courseUpdate(request):
    if request.method == "POST":
        courseId = request.POST['course_id']
        courseName = request.POST['name']
        duration = request.POST['duration']

        course = Course.objects.get(id=courseId)
        course.name = courseName
        course.duration = duration
        course.save()

        messages.success(request,"Course Are Successfully Updated ...")
        request.session["name"] = course.name
        return redirect('courseList')

    return render(request,'Hod/course_list.html')


@login_required(login_url='/')
def courseDelete(request,id):
    course = Course.objects.get(id=id)
    course.delete()

    messages.success(request,'Course Are Successfully Deleted ...')
    request.session["name"] = course.name
    return redirect('courseList')

# =============== COURSE END =================================================

# =============== SESSION START ==============================================

@login_required(login_url='/')   
def sessionAdd(request):
    if request.method == "POST":
        startSession = request.POST['start']
        endSession = request.POST['end']

        sessionYear = Session_Year(
            startSession = startSession,
            endSession = endSession
        )
        sessionYear.save()

        messages.success(request,"Session Are Successfully Created...")
        request.session["name"] = sessionYear.startSession + " To "+ sessionYear.endSession
        return redirect('sessionAdd')  

    return render(request,"Hod/session_add.html")


@login_required(login_url='/')
def sessionList(request):
    sessionYear = Session_Year.objects.all()
    
    context = {
        'sessionYear' : sessionYear
    }

    return render(request,"Hod/session_list.html",context)


@login_required(login_url='/')
def sessionEdit(request,id):
    sessionYear = Session_Year.objects.get(id=id)

    context = {
        'sessionYear' : sessionYear
    }

    return render(request,'Hod/session_edit.html',context)

@login_required(login_url='/')
def sessionUpdate(request):
    if request.method == "POST":
        session_id = request.POST['sessionId']
        session_start = request.POST['start']
        session_end = request.POST['end']

        sessionYear = Session_Year(
            id=session_id,
            startSession = session_start,
            endSession = session_end,
            )
        sessionYear.save()

        messages.success(request,"Session Are Successfully Updated...")
        request.session["name"] = sessionYear.startSession + " To "+ sessionYear.endSession
        return redirect('sessionList')

    return render(request,'Hod/session_list.html')


@login_required(login_url='/')
def sessionDelete(request,id):
    sessionYear =  Session_Year.objects.get(id=id)
    sessionYear.delete()

    messages.success(request,"Session Are Successfully Deleted...")
    request.session["name"] = str(sessionYear.startSession) + " To "+ str(sessionYear.endSession)
    return redirect('sessionList')
    
# =============== SESSION END =================================================


# =============== STUDENT START ==============================================

@login_required(login_url='/')
def studentAdd(request):
    course = Course.objects.all()
    sessionYear = Session_Year.objects.all()

    if request.method == "POST":
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        phoneNo = request.POST['phone']
        address = request.POST['add']
        gender = request.POST['gender']
        dob = request.POST['dob']
        courseId = request.POST['course']
        sessionId = request.POST['session']
        profilePic = request.FILES.get('profile')
        password = request.POST['password']

        print(firstName,lastName,email,username,phoneNo,address,gender,dob,courseId,sessionId,profilePic)

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,"Email Is Already Used....")
            return redirect('studentAdd')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,"Username Is Already Used")
            return redirect('studentAdd')

        else:
            user = CustomUser(
                # models variable name = views.py variable name
                first_name = firstName,
                last_name = lastName,
                email = email,
                username = username,
                dob = dob,
                phone_no = phoneNo,
                address = address,
                profile_pic = profilePic,
                user_type = 3

            )
            user.set_password(password)
            user.save()

            courseName = Course.objects.get(id=courseId)
            sessionName = Session_Year.objects.get(id=sessionId)
            # print(courseId)    5
            # print(courseName)  BBA

            student = Student(
                admin=user,
                gender=gender,
                course_id=courseName,
                session_id=sessionName
            )
            student.save()

            messages.success(request,f"{user.first_name} {user.last_name} Student Record Are Successfully Added...")
            return redirect('studentAdd')


    context = {
        'course': course,
        'sessionYear': sessionYear,
    }
    
    return render(request,'Hod/student_add.html',context)


@login_required(login_url='/')
def studentList(request):
    student = Student.objects.all()

    context = {
        'student':student
    }
    
    return render(request,'Hod/student_list.html',context)


@login_required(login_url='/')
def studentEdit(request,id):
    student = Student.objects.get(id=id)
    course = Course.objects.all()
    sessionYear = Session_Year.objects.all()

    context = {
        'student' : student,
        'course' : course,
        'sessionYear' : sessionYear,
    }

    return render(request,'Hod/student_edit.html',context)


@login_required(login_url='/')
def studentUpdate(request):
    if request.method == "POST":
        student_id = request.POST['studentId']
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        phoneNo = request.POST['phone']
        address = request.POST['add']
        gender = request.POST['gender']
        dob = request.POST['dob']
        courseId = request.POST['course']
        sessionId = request.POST['session']
        profilePic = request.FILES.get('profile')
        password = request.POST['password']

        user = CustomUser.objects.get(id=student_id)
        user.first_name = firstName
        user.last_name = lastName
        user.email = email
        user.username = username
        user.phone_no = phoneNo
        user.dob = dob
        user.address = address

        if password != None and password != "":
            user.set_password(password)
        if profilePic != None and profilePic != "":
            user.profile_pic = profilePic
        user.save()

        courseName = Course.objects.get(id=courseId)
        sessionName = Session_Year.objects.get(id=sessionId)

        student = Student.objects.get(admin=student_id)
        student.gender = gender
        student.course_id = courseName
        student.session_id = sessionName
        student.save()

        messages.success(request,f"{user.first_name} {user.last_name}  Student Record Are Sucessfully Updated...")
        return redirect('studentList')

    return render(request,'Hod/student_list.html')


@login_required(login_url='/')
def studentDelete(request,id):
    student = CustomUser.objects.get(id=id)
    student.delete()

    messages.success(request,f"{student.first_name} {student.last_name}  Student Record Are Successfully Deleted...")
    return redirect('studentList')

# =============== STUDENT END =================================================


# =============== TEACHER START ==============================================


@login_required(login_url='/')
def teacherAdd(request):
    if request.method == "POST":
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        phoneNo = request.POST['phone']
        address = request.POST['add']
        dob = request.POST['dob']
        gender = request.POST['gender']
        qualification = request.POST['quali']
        experience = request.POST['experi']
        joinDate = request.POST['joinDate']
        profilePic = request.FILES.get('profile')
        password = request.POST['password']

        print(firstName,lastName,email,username,phoneNo,address,dob,gender,qualification,experience,joinDate,profilePic,password)

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,"Your Email Already Exists..")
            return redirect('teacherAdd')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request,"Your Username Already Exists..")
            return redirect('teacherAdd')

        else:
            user = CustomUser(
                first_name = firstName,
                last_name = lastName,
                email = email,
                username = username,
                profile_pic = profilePic,
                dob = dob,
                address = address,
                phone_no = phoneNo,
                user_type = 2,
                )
            user.set_password(password)
            user.save()

            teacher = Teacher(
                admin = user,
                gender = gender,
                qualification = qualification,
                experience = experience,
                joining_date = joinDate
            )
            teacher.save()

            messages.success(request,f"{user.first_name} {user.last_name}  Teacher's Record Are Successfully Added...")  

    return render(request,'Hod/teacher_add.html')


@login_required(login_url='/')
def teacherList(request):
    teacher = Teacher.objects.all()

    context = {
        'teacher':teacher
    }

    return render(request,'Hod/teacher_list.html',context)


@login_required(login_url='/')
def teacherEdit(request,id):
    teacher = Teacher.objects.get(id=id)

    context = {
        'teacher':teacher
    }
    
    return render(request,"Hod/teacher_edit.html",context)


@login_required(login_url='/')
def teacherUpdate(request):
    if request.method == "POST":
        teacher_id = request.POST['teacherId']
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        phoneNo = request.POST['phone']
        address = request.POST['add']
        dob = request.POST['dob']
        gender = request.POST['gender']
        qualification = request.POST['quali']
        experience = request.POST['experi']
        joinDate = request.POST['joinDate']
        profilePic = request.FILES.get('profile')
        password = request.POST['password']

        user = CustomUser.objects.get(id = teacher_id)
        user.first_name = firstName
        user.last_name = lastName
        user.email = email
        user.username = username
        user.dob = dob
        user.address = address
        user.phone_no = phoneNo

        if profilePic != None and profilePic != "":
            user.profile_pic = profilePic
        if password != None and password != "":
            user.set_password(password)
        user.save()


        teacher = Teacher.objects.get(admin=teacher_id)
        teacher.gender = gender
        teacher.qualification = qualification
        teacher.experience = experience
        teacher.joining_date = joinDate
        teacher.save()

        messages.success(request,f"{user.first_name} {user.last_name}  Teacher's Record Are Sucessfully Updated...")
        return redirect('teacherList')

    return render(request,'Hod/teacher_list.html')


@login_required(login_url='/')
def teacherDelete(request,id):
    teacher = CustomUser.objects.get(id=id)
    teacher.delete()

    messages.success(request,f"{teacher.first_name} {teacher.last_name}  Teacher's Record Are Sucessfully Deleted...")
    return redirect('teacherList')


# =============== TEACHER END =================================================


# =============== SUBJECT START ==============================================


@login_required(login_url='/')
def subjectAdd(request):
    course = Course.objects.all()
    teacher = Teacher.objects.all()

    if request.method == "POST":
        subjectName = request.POST['sub_name']
        courseId = request.POST['course_id']
        teacherId = request.POST['teacher_id']

        courseName = Course.objects.get(id=courseId)
        teacherName = Teacher.objects.get(id=teacherId)

        subject = Subject(
            name = subjectName,
            course_name = courseName,
            teacher_name = teacherName
        )
        subject.save()

        messages.success(request,f"{subject.name} Subject Are Successfully Added..")
        return redirect('subjectAdd')

    context = {
        'course' : course,
        'teacher' : teacher,
    }

    return render(request,'Hod/subject_add.html',context)


@login_required(login_url='/')
def subjectList(request):
    subject = Subject.objects.all()

    context = {
        'subject' : subject
    }

    return render(request,'Hod/subject_list.html',context)


@login_required(login_url='/')
def subjectEdit(request,id):
    subject = Subject.objects.get(id=id)
    course = Course.objects.all()
    teacher = Teacher.objects.all()
    
    context = {
        'subject' : subject,
        'course' : course,
        'teacher' : teacher,
    }

    return render(request,"Hod/subject_edit.html",context) 


@login_required(login_url='/')
def subjectUpdate(request):
    if request.method == "POST":
        subjectId = request.POST['sub_id']
        subjectName = request.POST['sub_name']


        courseId = request.POST['course_id'] # id=1 return id 
        courseName = Course.objects.get(id=courseId) # BE return Value

        teacherId = request.POST['teacher_id']
        teacherName = Teacher.objects.get(id=teacherId)

        subject = Subject.objects.get(id=subjectId)
        subject.name = subjectName
        subject.course_name = courseName
        subject.teacher_name = teacherName
        subject.save()

        messages.success(request,f"{subject.name} Subject Are Successfully Updated.. ")
        return redirect('subjectList')

    return render(request,"Hod/subject_list.html")


@login_required(login_url='/')
def subjectDelete(request,id):
    subject = Subject.objects.get(id=id)
    subject.delete()

    messages.success(request,f"{subject.name} Subject Are Successfully Deleted.. ")
    return redirect('subjectList')


# =============== SUBJECT END =================================================


# ================== TEACHER NOTIFICATIONS START ==================================

@login_required(login_url='/')
def teacherNotification(request):
    teacher = Teacher.objects.all()

    seeNotification = Teacher_Notification.objects.all().order_by('-id')

    context = {
        'teacher' : teacher,
        'seeNotification' : seeNotification
    }

    return render(request,'Hod/teacher_notification.html',context)


@login_required(login_url='/')
def saveTeacherNotification(request):
    if request.method == "POST":
        teacherId = request.POST['teacher_id']
        message = request.POST['msg']

        teacherId = Teacher.objects.get(admin=teacherId)

        teacherNotification = Teacher_Notification(
            teacher_id = teacherId,
            message = message
        )
        teacherNotification.save()

        messages.success(request,"Notifications Are Successfully Send")
        return redirect('teacherNotification')

    
# ================== TEACHER NOTIFICATIONS START ==================================