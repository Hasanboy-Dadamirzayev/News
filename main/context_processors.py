import requests
from .models import *

def get_weather(request):
    weather_data = requests.get(
        'https://api.weatherapi.com/v1/current.json?q=fergana&key=de5abe25d0634ec0a76124759252403'
    ).json()
    return {
        'weather': weather_data,
    }

def get_category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return context
