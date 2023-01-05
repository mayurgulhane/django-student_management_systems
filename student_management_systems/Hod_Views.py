from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Course,Session_Year

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
