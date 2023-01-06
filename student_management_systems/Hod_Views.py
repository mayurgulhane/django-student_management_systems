from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Course,Session_Year, CustomUser, Student

@login_required(login_url='/')
def hodHome(request):
    messages.success(request,"Log In Successfully..")
    return render(request,"Hod/hodHome.html")

# =============== COURSE START =========================================

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


def courseList(request):
    course = Course.objects.all()

    context = {
        'course': course
    }

    return render(request,'Hod/course_list.html',context)


def courseEdit(request,id):
    course = Course.objects.get(id = id)

    context = {
        'course':course
    }

    return render(request,'Hod/course_edit.html',context)


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


def courseDelete(request,id):
    course = Course.objects.get(id=id)
    course.delete()

    messages.success(request,'Course Are Successfully Deleted ...')
    request.session["name"] = course.name
    return redirect('courseList')

# =============== COURSE END =================================================

# =============== SESSION START ==============================================
    
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


def sessionList(request):
    sessionYear = Session_Year.objects.all()
    
    context = {
        'sessionYear' : sessionYear
    }

    return render(request,"Hod/session_list.html",context)


def sessionEdit(request,id):
    sessionYear = Session_Year.objects.get(id=id)

    context = {
        'sessionYear' : sessionYear
    }

    return render(request,'Hod/session_edit.html',context)

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


def sessionDelete(request,id):
    sessionYear =  Session_Year.objects.get(id=id)
    sessionYear.delete()

    messages.success(request,"Session Are Successfully Deleted...")
    request.session["name"] = str(sessionYear.startSession) + " To "+ str(sessionYear.endSession)
    return redirect('sessionList')
    
# =============== SESSION END =================================================


# =============== STUDENT START ==============================================

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


def studentList(request):
    student = Student.objects.all()

    context = {
        'student':student
    }
    
    return render(request,'Hod/student_list.html',context)


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


def studentDelete(request,id):
    student = CustomUser.objects.get(id=id)
    student.delete()

    messages.success(request,f"{student.first_name} {student.last_name}  Student Record Are Successfully Deleted...")
    return redirect('studentList')

# =============== STUDENT END =================================================