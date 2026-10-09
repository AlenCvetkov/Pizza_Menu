from django.shortcuts import render
from .models import Pizza
# Create your views here.

def pizza_list(request):
    classics = Pizza.objects.filter(category='classic')
    spicys = Pizza.objects.filter(category='spicy')
    veges = Pizza.objects.filter(category='vege')

    context = {
        'classics': classics,
        'spicys': spicys,
        'veges': veges,
    }
    return render(request, 'pizzas/pizza_list.html', context)