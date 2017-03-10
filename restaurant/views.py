from django.shortcuts import render
from django.template import Context, Template
from django.http import HttpResponseRedirect
from restaurant.models import Restaurant



def restaurants(request):
    try:
        restaurantList = Restaurant.objects.values()
        context = Context({'rests':restaurantList})
        return render(request, 'restaurant/restaurantList.html',context)
    except Restaurant.DoesNotExist:
        return render(request, 'restaurant/restaurantList.html')

