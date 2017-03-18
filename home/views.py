from django.shortcuts import render, render_to_response
from home.models import Users,Grade,Constants
from django.template import Context, Template
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from restaurant.models import Restaurant
from home.forms import UserForm
import logging
import requests

def home(request):
    flag = hava()
    return render(request, 'home/home.html')

def statistics(request):
     return render(request, 'home/statistics.html')

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
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/users/')
        else:
            form = RetaurantForm()
            return HttpResponseRedirect('/users/')

def gradeIt(request):
    if request.method == 'POST':
        clickedUserId = request.POST.get('user_id')
        rests = Restaurant.objects.values()
        return render(request, 'home/gradeIt.html',Context({'user':Users.objects.get(id=clickedUserId),'Restaurant':rests}))

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
        return HttpResponseRedirect('/grading/')

def saveGrades(request):
    if  request.method == 'POST':
         grades = request.POST.getlist('grade[]')
         rids = request.POST.getlist('rid[]')
         uid = request.POST.get('uid')
         userGrade =  Grade.objects.filter(user_id= uid)
         counter = len(grades)
         i=0

         if userGrade.exists():
             while i < counter:
                 Grade.objects.select_related().filter(user_id = uid, rest_id = rids[i]).update(grade = grades[i])
                 i = i + 1
         else:
             while i < counter:
                 newGrade = Grade(rest_id = rids[i], user_id = uid, grade = grades[i])
                 newGrade.save()
                 i = i + 1


    return HttpResponseRedirect('/grading/')

def hava():
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Istanbul&APPID=b9dd3952f36a165aecc5518e9e0a5117')
        deneme = r.json()
        tempKelvin = deneme['main']['temp']
        tempCelcius = tempKelvin - 273,15
        humidity = deneme['main']['humidity']
        weatherGroup = deneme['weather'][0]['main']
        weatherId = deneme['weather'][0]['id']
        if (weatherId >= 900 or (weatherId >= 600 and weatherId <=699 ) or (weatherId >= 200 and weatherId <= 299 ) or ( weatherId >= 501 and weatherId <=599 ) or ( weatherId >= 312 and weatherId <= 321 ) and weatherId == 302 ):
            return False
        return True




