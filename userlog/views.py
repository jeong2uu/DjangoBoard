# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect

from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from .models import User
from django.contrib.auth import authenticate, login, logout
import json
# Create your views here.

#로그인
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        print("body "+ str(request.body))
        userid = request.POST.get("userid", "")
        userpw = request.POST.get("userpw", "")

        result = authenticate(username=userid, password=userpw)
        print("userid = " + userid + " result = " + str(result))
        if result:
            #home.html url수정하기
            return redirect('../',login(request, result))
        else:
            return render(request, "userlog/index.html")
    return render(request, 'userlog/index.html')

#로그아웃
def logout_view(request):
    logout(request)
    return redirect('userlog:login')

#회원가입
#모든 값이 null일때 user객체를 만들면 안됨
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        firstName = request.POST.get("firstName", "")
        lastName = request.POST.get("lastName", "")
        # chkpasswd = request.POST.get("chkpasswd", "")
        email = request.POST.get("email", "")

        user = User.objects.create_user(username, email, password)
        user.first_name  = firstName
        user.last_name = lastName
        user.save()
        return redirect("userlog:login")    
    return render(request, 'userlog/signup.html')

@csrf_exempt
def duplicate_id(request):
    if request.method == 'POST' :
        data = json.loads(request.body)
        print(data)
        userid = data['username']
        print(userid)
        user = User.objects.all()
        if user.filter(username= userid).exists():
            duplicate = False
        else :
            duplicate = True
        print(duplicate)
        context = {'result' : duplicate, 'username': userid }
    return render(request, 'userlog/checkuserid.html', context)