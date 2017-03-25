from django.shortcuts import render, render_to_response
from home.models import Users,Grade,Constants
from django.template import Context, Template
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from threading import Thread
from django.utils import timezone
from restaurant.models import Restaurant
from home.forms import UserForm
from calculation.models import Result
import math,random,datetime
from django.db.models import F
import requests
import time
from random import randint
from django.core.mail import send_mail

def start(request):
    if request.method == 'POST':
        backGroundThread = backThread("Calculation")
        backGroundThread.start()
        return HttpResponseRedirect('/statistics')

class backThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name


    def run(self):
        standard()
        period = Constants.objects.get(name = 'period').value
        counter = period
        while counter > 0 :
            now = datetime.datetime.now()
            saat10 = now.replace(hour=10, minute=0, second=0, microsecond=0)
            saat1030 = now.replace(hour=10, minute=30, second=0, microsecond=0)
            if ((now > saat10) and (now < saat1030)) or counter == period:
                pickRest()
                counter = counter - 1

            time.sleep(1200) # 20 dk da bir kontrol ediyor


def app(request):
    return render(request,'header.html')

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


def standard():
    Result.objects.all().delete()
    users = Users.objects.all();
    period = Constants.objects.get(name = 'period')
    rcount = Restaurant.objects.all().count()
    pv = period.value
    if Constants.objects.filter(name = 'currentday').count() > 0:
        Constants.objects.filter(name='currentday').update(value = 1)
    else:
        newConstant = Constants(name='currentday', value = 1)
        newConstant.save()
        
    if Constants.objects.filter(name = 'isAlgorithmOn').count() > 0:
        Constants.objects.filter(name='isAlgorithmOn').update(value = 1)
    else:
        newConstant = Constants(name='isAlgorithmOn', value = 1)
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

def pickRest():
    currentDay = Constants.objects.get(name = 'currentday')
    cDay = currentDay.value
    w_c = hava()


    musaitRests = Restaurant.objects.filter(counter__gt = 0).order_by('-counter')
    
    if cDay > 1 and musaitRests.count() != 1 : # onceki gun ile ayni olmasin
        formerRest = Result.objects.last()
        restId = formerRest.rest_id
        musaitRests = musaitRests.exclude(id = restId)

    if w_c == False and musaitRests.count() != 1: # hava guzel olsun
        musaitRests = musaitRests.exclude(weatherSensetion = True)

    if cDay == 2 and musaitRests.count() != 1 : #transportation control
        formerRest = Result.objects.get(day = (cDay-1))
        rest = Restaurant.objects.get(id = formerRest.rest_id)

        if rest.transportation:
            musaitRests = musaitRests.exclude(transportation = True)

    elif cDay > 2: # transportation control
        formerRest1 = Result.objects.get(day = (cDay-1))
        rest1 = Restaurant.objects.get(id = formerRest1.rest_id)

        formerRest2 = Result.objects.get(day = (cDay-2))
        rest2 = Restaurant.objects.get(id = formerRest2.rest_id)

        if (rest1.transportation or rest2.transportation) and musaitRests.count() != 1 :
            musaitRests = musaitRests.exclude(transportation = True)
    
    period = Constants.objects.get(name = 'period')
    pv = period.value
    
    remainingDay = pv - cDay
    remainingBadWDay = 0
    rests = Restaurant.objects.filter(weatherSensetion = True)
    for r in rests:
        remainingBadWDay = remainingBadWDay + r.counter
    
    remainingCarDay = 0
    rests = Restaurant.objects.filter(transportation = True)
    for r in rests:
        remainingCarDay = remainingCarDay + r.counter
        
    if remainingBadWDay * 2 > remainingDay:
        restcount = musaitRests.filter(weatherSensetion = True).count()
        if restcount > 0 :
            musaitRests = musaitRests.exclude(weatherSensetion = False)
        
    if remainingCarDay * 3 > remainingDay:
         restcount = musaitRests.filter(transportation = True).count()
         if restcount > 0 :
            musaitRests = musaitRests.exclude(transportation = False)
        
        
    if musaitRests.count() == 0: # elemeler sonunda sonuc bulamadiysak kalanlarin hepsini getir
        musaitRests = Restaurant.objects.filter(counter__gt = 0)
        
        
    min = musaitRests.last()
    perfectRate = min.totalDay / pv
    if cDay < pv:
        for rests in musaitRests:
            rate = rests.counter/(pv - cDay)
            if musaitRests.count() > 1 and rate< perfectRate:
                musaitRests = musaitRests.exclude(id = rests.id)
    
    rlist = []
    for m in musaitRests:
       for count  in range(0,m.counter):
          rlist.append(m.id)

    index = random.choice(rlist)
    while index == 0:
        index = random.choice(rlist)

    cr = Restaurant.objects.get(id = index)
    cr.counter -= 1
    cr.save()
    

    newResult = Result(rest_id = cr.id, day = cDay, date = datetime.datetime.now(), weather = w_c)
    newResult.save()

    currentDay = Constants.objects.get(name = 'currentday')
    currentDay.value += 1
    currentDay.save()
    
    Res = Result.objects.get(day = cDay)
    kullanici = Users.objects.all()
   
    for k in kullanici:
            send_mail('Gunun Restauranti', 'Tarih:' + str(Res.date) + ' ---> Bugunun restauranti: ' + str(Res.rest.name), 'noreply.neredeyesek@gmail.com', [k.userMail], fail_silently=False)


