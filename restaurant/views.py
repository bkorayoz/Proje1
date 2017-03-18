from django.shortcuts import render
from django.template import Context, Template
from django.http import HttpResponseRedirect
from restaurant.models import Restaurant
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
            return HttpResponseRedirect('/restaurants/')

    else:
        form = RetaurantForm()
        return HttpResponseRedirect('/restaurants/')

def deleteRestaurant(request, id):
    query = Restaurant.objects.get(pk= id)
    query.delete()
    return HttpResponseRedirect('/restaurants/')
#
