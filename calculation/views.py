from django.shortcuts import render, render_to_response
from home.models import Users,Grade,Constants
from django.template import Context, Template
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from restaurant.models import Restaurant
from home.forms import UserForm
from calculation.models import Result
import math,random,datetime
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
        Restaurant.objects.filter(id = r.id).update(counter = floorgrade[i], totalDay = floorgrade[i])
        i = i+1
        
    overDay = pv - sum(floorgrade)
    
    while overDay > 0:
        index = decimalgrade.index(max(decimalgrade))
        floorgrade[index] = floorgrade[index] + 1
        Restaurant.objects.filter(id = restidgrade[index]).update(counter = floorgrade[index], totalDay = floorgrade[index])
        overDay = overDay - 1
        decimalgrade[index] = 0
    
    
    users_value = Grade.objects.values()
    rest_value = Restaurant.objects.values()
    #counter valuelar ayarlandi 
    return render(request, 'calculation/standard.html',Context({'grades': users_value,'rest': rest_value, 'floor': floorgrade,'decimal': decimalgrade}))

def pickRest():
    
    currentDay = Constants.objects.get(name = 'currentday')
    cDay = currentDay.value
    
    musaitRests = Restaurant.objects.filter(counter__gt = 0)
    
    if cDay > 1:
        formerRest = Result.objects.get(day = (cDay-1))
        restId = formerRest.rest_id
        musaitRests = musaitRests.exclude(id = restId)
        
    if not hava():
        musaitRests = musaitRests.exclude(weatherSensation = True)
         
    if cDay == 2:
        formerRest = Result.objects.get(day = (cDay-1))
        rest = Restaurant.objects.get(id = formerRest)
        
        if rest.transportation:
            musaitRests = musaitRests.exclude(transportation = True)
     
    elif cDay > 2:
        formerRest1 = Result.objects.get(day = (cDay-1))
        rest1 = Restaurant.objects.get(id = formerRest1)
        
        formerRest2 = Result.objects.get(day = (cDay-2))
        rest2 = Restaurant.objects.get(id = formerRest2)
        
        if rest1.transportation or rest2.transportation:
            musaitRests = musaitRests.exclude(transportation = True)

    
    if musaitRests.count() == 0:
        musaitRests = Restaurant.objects.filter(counter__gt = 0)
         
    period = Constants.objects.get(name = 'period')
    pv = period.value
    
    rlist = [None] * (pv - cDay + 1)
    i = 0
    for m in musaitRests:
       tempi = i
       for count  in range(tempi,m.counter):
           rlist[count] = m.id
           i += 1
     
    index = random.choice(rlist)
    
    cr = Restaurant.objects.get(id = index)
    cr.counter -= 1
    cr.save()
    
    newResult = Result(rest_id = index, day = cDay, date = datetime.datetime.now())
    newResult.save()
    
    currentDay = Constants.objects.get(name = 'currentday')
    currentDay.value += 1
    currentDay.save()
    
    return index
     
