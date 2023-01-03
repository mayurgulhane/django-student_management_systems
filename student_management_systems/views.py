from django.shortcuts import render, redirect,HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def LogIn(request):
    return render(request,"logIn.html")

def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,
                                        username = request.POST['email'],
                                        password = request.POST['pass1'],
                                        )
        if user != None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return HttpResponse('HOD')
            elif user_type == '2':
                return HttpResponse("Teacher")
            elif user_type == '3':
                return HttpResponse('Student')
            else:
                messages.error(request,"Invalid ")
                return redirect('LogIn')
        else:
            messages.error(request,"Invalid email or password")
            return redirect('LogIn')