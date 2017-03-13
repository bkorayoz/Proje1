from django.shortcuts import render
from django.template import Context, Template
from django.http import HttpResponseRedirect
from restaurant.models import Restaurant
from django.template.context_processors import request




def restaurants(request):
    try:
        restaurantList = Restaurant.objects.values()
        context = Context({'rests':restaurantList})
        return render(request, 'restaurant/restaurantList.html',context)
    except Restaurant.DoesNotExist:
        return render(request, 'restaurant/restaurantList.html')

#def addRetaurant(request):
#    if request.method == 'POST':
#        form = Restaurant(request.POST)
#
#       if form.is_valid():
#
