from django.shortcuts import render, render_to_response
from home.models import Users,Grade,Constants
from django.template import Context, Template
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from restaurant.models import Restaurant
from calculation.models import Result
from home.forms import UserForm
from calculation.views import backThread
import logging
import requests

def home(request):
    if request.method == 'POST':
        backGroundThread = backThread("Calculation")
        backGroundThread.start()
        return HttpResponseRedirect('/statistics')
    return render(request, 'home/home.html')

def statistics(request):
     rests = Restaurant.objects.values()
     results = Result.objects.all()
     cday = Constants.objects.filter(name = 'currentday').values()
     period = Constants.objects.filter(name = 'period').values()
     return render(request, 'home/statistics.html', Context({'period':period,'cday': cday,'rests': rests,'results': results}))

def grading(request):
     users = Users.objects.values()
     users_all = Users.objects.all()
     flag = True
     for u in users_all:
         u_temp = Grade.objects.filter(user_id = u.id)
         if not u_temp:
             flag = False

     return render(request, 'home/grading.html',Context({'IsGradingDone':flag,'period':Constants.objects.filter(name = 'period'),'Users':users}))

def users(request):
    try:
        users = Users.objects.values()
        return render(request, 'home/users.html',Context({'Users':users}))
    except Users.DoesNotExist:
        return render(request, 'home/users.html')
def deleteUser(request, id):
    query = Users.objects.get(pk=id)
    query.delete()
    return HttpResponseRedirect('/users/')

def addUser(request):
     if request.method == 'POST':
        enteredUserName = request.POST.get('userName', None)
        enteredEmail = request.POST.get('userMail', None)
        try:
            data = Users.objects.get(userName = enteredUserName)
        except Users.DoesNotExist:
            newUser = Users(userName = enteredUserName, userMail = enteredEmail, flag = False)
            newUser.save()
            return HttpResponseRedirect('/users/')
        return HttpResponseRedirect('/users/')
     else:
        return HttpResponseRedirect('/users/')

def gradeIt(request):
    if request.method == 'POST':
        clickedUserId = request.POST.get('user_id')
        rests = Restaurant.objects.values()
        period = Constants.objects.get(name = 'period')
        return render(request, 'home/gradeIt.html',Context({'pvaluehalf': period.value/2,'pvalue': period.value,'user':Users.objects.get(id=clickedUserId),'Restaurant':rests}))

def enterPeriod(request):
    if request.method == 'POST':
        entered_period = request.POST.get('period')
        checkperiod = Constants.objects.filter(name = 'period')
        if checkperiod.exists():
            Constants.objects.get(name = 'period').update(value = entered_period)
        else:
            newCons = Constants(name = 'period', value = entered_period)
            newCons.save()

        return HttpResponseRedirect('/grading/')

def editPeriod(request):
    if  request.method == 'POST':
        Grade.objects.all().delete()
        Constants.objects.filter(name = 'period').delete()
        Users.objects.all().update(flag = False)
        return HttpResponseRedirect('/grading/')

def saveGrades(request):
    if  request.method == 'POST':
         grades = request.POST.getlist('grade[]')
         rids = request.POST.getlist('rid[]')
         uid = request.POST.get('uid')
         userGrade =  Grade.objects.filter(user_id= uid)
         period = Constants.objects.get(name = 'period')
         pv = period.value
         counter = len(grades)
         controlFlag = True
         count = 0
         i = 0
         for g in grades:
              count = count +int(g)
         if count > pv:
            controlFlag = False

         for g in grades:
            if int(g) > count/2:
                controlFlag = False

         if controlFlag:
             Users.objects.filter(id = uid).update(flag = True)

             if userGrade.exists():
                 while i < counter:
                     Grade.objects.select_related().filter(user_id = uid, rest_id = rids[i]).update(grade = grades[i])
                     i = i + 1
             else:
                 while i < counter:
                     newGrade = Grade(rest_id = rids[i], user_id = uid, grade = grades[i])
                     newGrade.save()
                     i = i + 1
         #else:
            # HATALI GIRIS

    return HttpResponseRedirect('/grading/')




