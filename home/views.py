from django.shortcuts import render, render_to_response
from home.models import Users
from django.template import Context, Template
from django.http import HttpResponseRedirect
from django.contrib import messages
from restaurant.models import Restaurant
def home(request):
    return render(request, 'home/home.html')

def statistics(request):
     return render(request, 'home/statistics.html')
 
def grading(request):
     users = Users.objects.values()
     rests = Restaurant.objects.values()
     return render(request, 'home/grading.html',Context({'Users':users,'Restaurant':rests}))
 
def users(request):
    try:
        users = Users.objects.values()
        return render(request, 'home/users.html',Context({'Users':users}))
    except Users.DoesNotExist:
        return render(request, 'home/users.html')
def deleteUser(request):
    if request.method == 'POST':
        delete_this_id = request.POST.get('id', None)
        Users.objects.filter(id=delete_this_id).delete()
        return HttpResponseRedirect('/users/')
 
def addUser(request):
     if request.method == 'POST':
        enteredUserName = request.POST.get('userName', None)
        enteredEmail = request.POST.get('userMail', None)
        
        try:
            data = Users.objects.get(userName = enteredUserName)
        except Users.DoesNotExist:
            newUser = Users(userName = enteredUserName, userMail = enteredEmail)
            newUser.save()
            return HttpResponseRedirect('/users/')
        
        return HttpResponseRedirect('/users/')
     else:
        return HttpResponseRedirect('/users/')