from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django import forms
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
import googlemaps
from datetime import datetime
import numpy as np
from coordinates import Coordinate
import requests
import math
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import User, Place



# HERE MAPS API INFORMATION
# APP ID: BorZ7tKdXL8ZviCL3C9C
# API Key: iDgC0zva6sCVmG3VUpx3xlBNfcifckA3eDJPkB0AxP0

# GOOGLE MAPS API INFO
# API Key: AIzaSyBkZPjU2wlKG0goYDPx23xno37sCM42AJI

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('plotter:login'))

def register_view(request):
    if request.method == 'POST':
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mail/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, username, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "plotter/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("plotter:index"))
    else:
        return render(request, "plotter/register.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("plotter:index"))
        
        else:
            return render(request, 'plotter/login.html', {
                "message": "Invalid username and/or password."
            })
    
    else:
        return render(request, 'plotter/login.html')

        
    
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, "plotter/index.html")
    
    else:
        return HttpResponseRedirect(reverse('plotter:login'))


def search(request):
    if request.method == "GET":
        return render(request, 'plotter/search.html')

    if request.method == "POST": 
        csrf_token = request.META.get('HTTP_X_CSRFTOKEN')
        data = json.loads(request.body)
        addresses = data.get('addresses')
        filter = str(data.get('filter'))
        saved_data = data.get('saved_data')
        saved_lat = round(saved_data['lat'], 5)
        saved_lng = round(saved_data['lng'], 5)
        total = saved_data['total']


        if addresses == [""]:
            return JsonResponse({
                "error": "At least one recipient required."
            }, status=400)

    x_coords = []
    y_coords = []
        
    for address in addresses:
        gmaps = googlemaps.Client(key='AIzaSyBkZPjU2wlKG0goYDPx23xno37sCM42AJI')

        # Geocoding an address
        geocode_result = gmaps.geocode(address)

        coordinates = geocode_result[0]['geometry']['location']
        lat = coordinates['lat']
        lng = coordinates['lng']

        x_coords.append(lat)
        y_coords.append(lng)

    length = len(x_coords)

    centroid_x = float((sum(x_coords) + saved_lat) / (length + total))
    centroid_y = float((sum(y_coords) + saved_lng) / (length + total))

    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyBkZPjU2wlKG0goYDPx23xno37sCM42AJI&location={centroid_x},{centroid_y}&type={filter}&rankby=distance'
    # url = https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyBkZPjU2wlKG0goYDPx23xno37sCM42AJI&location=1.32648635,103.8572391&radius=1500

    # https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyBkZPjU2wlKG0goYDPx23xno37sCM42AJI&location=1.2909371778396834,103.84526132482546&radius=6.0&type=bar

       

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        places = response.json()
        places = places['results']
        places_data = []


        for place in places:
            # Remove first result which is just Sg
            if place['name'] != 'Singapore':
                try:
                    link = place['photos'][0]['html_attributions'][0]
                    link = link[9:]
                    photo = ""
                    for char in link:
                        if char == '"':
                            break
                        else:
                            photo = photo + char
                except:
                    photo = ""

                lat = float(place['geometry']['location']['lat'])
                lng = float(place['geometry']['location']['lng'])

                dist = coordDist(lat, lng, centroid_x, centroid_y)

                result = {'name': place['name'], 'vic': place['vicinity'], 'types': place['types'], 'dist': dist, 'photo': photo}
                places_data.append(result)

        
    except requests.exceptions.RequestException as e:
        print('THE EXCEPT ERROR')

    centroid = [centroid_x, centroid_y]
    data = {'centroid': centroid, 'addresses': addresses, 'places': places_data} 

    return JsonResponse({"message": "Midpoint found", "data": data}, status=201)


def coordDist(lat1, lng1, lat2, lng2):
    earth_rad = 6371

    lat_dist = math.radians(lat2-lat1)
    lng_dist = math.radians(lng2-lng1)

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = ( math.sin(lat_dist/2)**2 ) + ( math.sin(lng_dist/2)**2 * math.cos(lat1) * math.cos(lat2) )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


    return round(earth_rad * c, 2)

    
def load_places(request):
    user = request.user
    places = Place.objects.filter(user=user)
    data = []
    for place in places:
        name = place.name
        address = place.address
        lat = place.lat
        lng = place.lng
        pair = {'name': name, 'address': address, 'lat': lat, 'lng':lng}
        data.append(pair)
    
    return JsonResponse({'data': data}, status=201)


def add_place(request):
    csrf_token = request.META.get('HTTP_X_CSRFTOKEN')
    data = json.loads(request.body)
    user = request.user

    new_name = data.get('name')
    new_address = data.get('address')

    gmaps = googlemaps.Client(key='AIzaSyBkZPjU2wlKG0goYDPx23xno37sCM42AJI')
    # Geocoding an address
    geocode_result = gmaps.geocode(new_address)

    new_coordinates = geocode_result[0]['geometry']['location']
    new_lat = new_coordinates['lat']
    new_lng = new_coordinates['lng']


    old_data = Place.objects.filter(user=user)
    
    name_check  = True
    address_check = True
    for pair in old_data:
        if pair.name == new_name:
            name_check = False
            error = 'Place name already exists.'

        if pair.address == new_address:
            address_check = False
            error = 'Place address already exists'

    if (name_check is False) and (address_check is False):
        error = 'Place name and address are already in use.'
        
    if (name_check is True) and (address_check is True):
        place = Place(
            user=user,
            name=new_name,
            address=new_address,
            lat=new_lat,
            lng=new_lng
        )
        place.save()
        return JsonResponse({'message': 'Place created successfully.'}, status=201)
        
    else:
        return JsonResponse({'message': f'Error: {error}'}, status=201)

def delete_place(request):
    csrf_token = request.META.get('HTTP_X_CSRFTOKEN')
    data = json.loads(request.body)
    user = request.user

    print(data)

    try:
        place = Place.objects.filter(user=user, name=data)
        place.delete()
        return JsonResponse({'message': 'Successfully Deleted.'}, status=201)

    except:
        return JsonResponse({'message': 'ERROR OCCURED'}, status=201)