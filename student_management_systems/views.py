from django.shortcuts import render, redirect,HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import CustomUser

def LogIn(request):
    return render(request,"logIn.html")

def doLogIn(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,
                                        username = request.POST['email'],
                                        password = request.POST['pass1'],
                                        )
        if user != None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('hodHome')
            elif user_type == '2':
                return HttpResponse("Teacher")
            elif user_type == '3':
                return HttpResponse('Student')
            else:
                messages.error(request,"Invalid User Type ")
                return redirect('LogIn')
        else:
            messages.error(request,"Invalid email or password")
            return redirect('LogIn')
        
def doLogOut(request):
    logout(request)
    messages.success(request,"Log Out Successfully..")
    return redirect('LogIn')


@login_required(login_url='/')
def userProfile(request):
    user = CustomUser.objects.get(id = request.user.id)
    print(user.profile_pic)
    context ={
        'user':user
    }
    return render(request,"profile.html",context)


@login_required(login_url='/')
def profileUpdate(request):
    if request.method == "POST":
        firstName = request.POST['fname']
        lastName = request.POST['lname']
        email = request.POST['email']
        userName = request.POST['username']
        phoneNo = request.POST['phone']
        dob = request.POST['dob']
        address = request.POST['add']
        profilePic = request.FILES.get('profilePic')
        password = request.POST['pass1']
        print(firstName,lastName,email,userName,phoneNo,dob,address,profilePic,password)
        try:
            customUser = CustomUser.objects.get(id = request.user.id)
            print(customUser) 
            print(customUser.first_name)
            customUser.first_name = firstName
            customUser.last_name = lastName
            customUser.phone_no = phoneNo
            customUser.dob = dob
            customUser.address = address

            if password != None and password != "":
                customUser.set_password(password)
            if profilePic != None and profilePic != "":
                customUser.profile_pic = profilePic
            
            customUser.save()
            messages.success(request,"Your Profile Updated Successfully..")
            return redirect('userProfile')
        except:
            messages.error(request, 'Failed to Update Your Profile')
    return render(request,'profile.html')