import requests  # Library for making HTTP requests
from rest_framework.decorators import api_view
from rest_framework.response import Response  # Class to create response objects for API views
from django.conf import settings
from .models import Item
from .serializers import ItemSerializer
from rest_framework import status


@api_view(['GET'])
def test(request):
    data = {
        'name': 'Test API',
        'message': 'This is my first API endpoint'
    }
    return Response(data)


@api_view(['GET'])
def get_items(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def post_items(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['PATCH'])
def patch_item(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ItemSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_items(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        item.delete()
        return Response({'message': 'Item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def hello(request):
    visitor_name = request.GET.get('visitor_name', 'guest')
    open_weathermap_api_key = settings.OPEN_WEATHERMAP_API_KEY

    # Get client's external IP address from request headers
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # Header for proxy forwarded requests
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
        print(client_ip)
    else:
        client_ip = request.META.get('REMOTE_ADDR')  # Client IP if request is not forwarded
        print('error')

    # Fetch location based on IP
    if client_ip:
        try:
            ip_info_response = requests.get(f'http://ipinfo.io/{client_ip}')
            ip_info_response.raise_for_status()
            ip_info_data = ip_info_response.json()
            location = ip_info_data.get('city', 'Unknown location')
            print(f'IP Info response: {ip_info_data}')
        except requests.RequestException as e:
            print(f'Error fetching IP info: {e}')
            location = 'Unknown location'

        if location != 'Unknown location':
            try:
                weather_response = requests.get(
                    f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={open_weathermap_api_key}&units=metric')
                weather_response.raise_for_status()  # Check HTTP errors
                weather_data = weather_response.json()
                temperature = weather_data.get('main', {}).get('temp', 'Unknown')
                print(f'Weather response: {weather_data}')

            except requests.RequestException as e:
                print(f'Error fetching weather data: {e}')
                temperature = 'unknown'

        else:
            temperature = 'Unknown'
    else:
        location = 'Unknown location'
        temperature = 'Unknown'

    # Response data
    response_data = {
        'client_ip': client_ip,
        'location': location,
        'message': f'Hello {visitor_name}, the temperature is {temperature} degrees celcius in {location}'
    }

    print(f'Response data: {response_data}')

    return Response(response_data)
