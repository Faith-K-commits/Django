import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.conf import settings


def hello(request):
    name = request.GET.get('name', 'world')
    data = {'message': f'Hello, {name}!'}
    return JsonResponse(data)


@require_GET
def get_client_info(request):
    client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    ipstack_api_key = settings.IPSTACK_API_KEY
    weather_api_key = settings.WEATHER_API_KEY
    if client_ip == '127.0.0.1':
        client_ip = '8.8.8.8'

    ipstack_url = f'http://ipinfo.io/{client_ip}?token={ipstack_api_key}'
    ipstack_response = requests.get(ipstack_url).json()

    if 'error' in ipstack_response:
        return JsonResponse({'error': 'Unable to determine location'})

    city = ipstack_response.get('city', 'Unknown location')

    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={weather_api_key}'
    weather_response = requests.get(weather_url).json()

    print(weather_response)  # Debugging line

    if weather_response.get('cod') != 200:
        return JsonResponse({'error': 'Unable to fetch weather information', 'details': weather_response})

    if 'weather' not in weather_response:
        return JsonResponse({'error': 'Weather data is missing from the response', 'details': weather_response})

    weather = weather_response['weather'][0]['description']
    temperature = weather_response['main']['temp']

    data = {
        'client_ip': client_ip,
        'location': city,
        'message': f'The weather is {weather} and the temperature is {temperature} degrees celcius in {city}'
    }

    return JsonResponse(data)
