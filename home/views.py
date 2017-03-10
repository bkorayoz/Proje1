from django.shortcuts import render
from home.models import Users
from django.template import Context, Template
from django.http import HttpResponseRedirect

def home(request):
    return render(request, 'home/home.html')

def statistics(request):
     return render(request, 'home/statistics.html')
 
def grading(request):
     return render(request, 'home/grading.html')
 
def users(request):
    try:
        users = Users.objects.values()
        context = Context({'Users':users})
        return render(request, 'home/users.html',context)
    except Users.DoesNotExist:
        return render(request, 'home/users.html')
 
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
     else:
        return render(request, 'users')