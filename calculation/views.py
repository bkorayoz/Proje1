from django.shortcuts import render, render_to_response
from home.models import Users,Grade,Constants
from django.template import Context, Template
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from restaurant.models import Restaurant
from home.forms import UserForm
from calculation.models import Result
import math
from django.db.models import F
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


def standard(request):
    users = Users.objects.all();
    period = Constants.objects.get(name = 'period')
    rcount = Restaurant.objects.all().count()
    pv = period.value
    
    newConstant = Constants(name='currentday', value = 1)
    newConstant.save()
    
    for u in users:
        grades = Grade.objects.filter(user_id = u.id)
        
        sumgrades =0
        for g in grades:
            sumgrades = sumgrades + g.grade
            
        if sumgrades ==0:
            temp = pv / rcount
            Grade.objects.filter(user_id= u.id).update(grade = temp)
            
        else:
            oran = float(pv) / float(sumgrades)
            for g in grades:
                newgrade = oran * g.grade
                Grade.objects.filter(user_id = u.id, rest_id = g.rest_id).update(grade = newgrade)
                
                
    rests = Restaurant.objects.all()
    ucount = Users.objects.all().count()
    
    floorgrade = [None]* rcount
    decimalgrade = [None] * rcount
    restidgrade = [None] *rcount
    i=0
    
    for r in rests:
        gradesr = Grade.objects.filter(rest_id = r.id)
        sumgrades =0
        for g in gradesr:
            sumgrades = sumgrades + g.grade
        newCounterValue = sumgrades / ucount
        restidgrade[i] = r.id
        floorgrade[i] = math.floor(newCounterValue)
        decimalgrade[i] = newCounterValue - floorgrade[i]
        Restaurant.objects.filter(id = r.id).update(counter = floorgrade[i])
        i = i+1
        
    overDay = pv - sum(floorgrade)
    
    while overDay > 0:
        index = decimalgrade.index(max(decimalgrade))
        floorgrade[index] = floorgrade[index] + 1
        Restaurant.objects.filter(id = restidgrade[index]).update(counter = floorgrade[index])
        overDay = overDay - 1
        decimalgrade[index] = 0
    
    
    users_value = Grade.objects.values()
    rest_value = Restaurant.objects.values()
    return render(request, 'calculation/standard.html',Context({'grades': users_value,'rest': rest_value, 'floor': floorgrade,'decimal': decimalgrade}))
