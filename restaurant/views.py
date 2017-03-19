from django.shortcuts import render
from django.template import Context, Template
from django.http import HttpResponseRedirect
from restaurant.models import Restaurant
from home.models import Grade,Users
from django.template.context_processors import request
from restaurant.forms import RestaurantForm


def restaurants(request):
    try:
        restaurantList = Restaurant.objects.values()
        context = Context({'rests':restaurantList})
        return render(request, 'restaurant/restaurantList.html',context)
    except Restaurant.DoesNotExist:
        return render(request, 'restaurant/restaurantList.html')


def addRestaurant(request):

    if request.POST:
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            Grade.objects.all().delete()
            Users.objects.all().update(flag = False)
            return HttpResponseRedirect('/restaurants/')

    else:
        form = RestaurantForm()
        return HttpResponseRedirect('/restaurants/')

def deleteRestaurant(request, id):
    query = Restaurant.objects.get(pk= id)
    query.delete()
    Grade.objects.all().delete()
    Users.objects.all().update(flag = False)
    return HttpResponseRedirect('/restaurants/')
#
