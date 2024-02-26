from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.contrib import messages
import requests
import datetime


# Create your views here.
def home(request):
    popular_cities = {
        'Kaunas': 'kaunas',
    }

    if 'city' in request.POST:
        city = request.POST['city']
    elif 'popular_city' in request.GET:
        city = request.GET['popular_city']
    else:
        city = 'kaunas'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=01af3ddd31c114471a2d6f9eb4b1fe15'
    PARAMS = {'units': 'metric'}  # pakeicia units i europietiska matavima

    try:
        data = requests.get(url, params=PARAMS).json()

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        humidity = data['main']['humidity']
        feels_like = data['main']['feels_like']
        day = datetime.date.today()

        context = {
            'city': city,
            'popular_cities': popular_cities,
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'wind_speed': wind_speed,
            'humidity': humidity,
            'feels_like': feels_like,
            'exception_occured': False
        }
        return render(request, 'index.html', context=context)

    except:
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()

        context = {
            'description': '-',
            'icon': '-',
            'temp': '-',
            'day': day,
            'city': 'City does not exists',
            'exception_occurred': exception_occurred
        }

    return render(request, 'index.html', context=context)


def get_city_by_coords(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=01af3ddd31c114471a2d6f9eb4b1fe15'
    PARAMS = {'units': 'metric'}

    try:
        data = requests.get(url, params=PARAMS).json()
        city = data.get('name', 'Unknown City')
        return JsonResponse({'city': city})
    except:
        return JsonResponse({'city': 'Unknown City'})
