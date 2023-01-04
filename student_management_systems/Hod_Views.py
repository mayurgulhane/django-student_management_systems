from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/')
def hodHome(request):
    messages.success(request,"Log In Successfully..")
    return render(request,"Hod/hodHome.html")