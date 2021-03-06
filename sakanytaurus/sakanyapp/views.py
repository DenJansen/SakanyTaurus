from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from . import secrets
from .models import UserRoute, RouteStep

import requests
import json

# Create your views here.
#
# def register(request):
#     return render(request, 'users/register.html')
#
# def register_user(request):
#     username = request.POST['username']
#     email = request.POST['email']
#     password = request.POST['password']
#     user = User.objects.create_user(username, email, password)
#     login(request, user)
#     return HttpResponseRedirect(reverse(''))

# Renders login page
def login_page(request):
    message = request.GET.get('message', '')
    next = request.GET.get('next', '')
    context = {
        'next': next, #redirects to previously-viewed pages
        'message': message
    }
    return render(request, 'sakanyapp/login.html', context)

# User authentication
def user_login (request):
    next = request.POST['next']
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if next != '':
            return HttpResponseRedirect(next)
        return HttpResponseRedirect(reverse('sakanyapp:index'))
    if next == '':
        return HttpResponseRedirect(reverse('sakanyapp:login') + '?message=failure')
    return HttpResponseRedirect(reverse('sakanyapp:login') + '?message=failure&next='+next)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('sakanyapp:login'))

@login_required
def index(request):
    context = {
        'mapapi': secrets.mapapi #calls map api for use with Google Maps
    }
    return render(request, 'sakanyapp/index.html', context)

# Conduct API pulls of Google Maps and Yelp APIs
@login_required
def findpub(request):
    save_json = json.loads(request.body)
    address = save_json['address']
    #access api using address string and api key
    map_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={secrets.mapapi}'
    map_response = requests.get(map_url)
    #pull coordinates
    geocoords = json.loads(map_response.text)['results'][0]['geometry']['location']

    yelpurl = f"https://api.yelp.com/v3/businesses/search?latitude={geocoords['lat']}&longitude={geocoords['lng']}&sort_by=distance&categories=breweries,brewpubs,beerbar,divebars,irish_pubs,pubs,beergarden,beergardens,barcrawl,beerhall"

    yelpheaders = {'Authorization': 'Bearer %s' % secrets.yelpapi}
    yelpresponse = requests.get(yelpurl, headers=yelpheaders)
    yelpdata = json.loads(yelpresponse.text)['businesses']
    #
    origin = (geocoords['lat'],geocoords['lng'])

    return JsonResponse({'pubresults':yelpdata,'origin':origin})

# Saves user-create pub crawl route
@login_required
def newcrawl(request):
    json_data = json.loads(request.body)
    pub_route = json_data['pub_route']
    route = json_data['crawlname']
    print(json_data['pub_route'])
    print(json_data['crawlname'])

    newcrawl = UserRoute(creator=request.user, name=route)
    newcrawl.save()

    order_num = 0
    for pub in pub_route:
        order_num += 1
        loc_name = pub['name']
        loc_rating = pub['rating']
        print(pub['location']['display_address'])
        loc_address = ', '.join(pub['location']['display_address'])
        loc_lat = pub['coordinates']['latitude']
        loc_lon = pub['coordinates']['longitude']
        distance = pub['distance']
        newdistance = float(pub['newdistance'])
        unit = pub['unit']
        stars = pub['stars']
        halfstar = pub['halfstar']
        review_count = pub['review_count']

        create_crawl = RouteStep(route=newcrawl, order_num=order_num, loc_name=loc_name, loc_rating=loc_rating, loc_address=loc_address, loc_lat=loc_lat, loc_lon=loc_lon, distance=distance, newdistance=newdistance, unit=unit, stars=stars, halfstar=halfstar, review_count=review_count)
        create_crawl.save()

    return HttpResponseRedirect(reverse('sakanyapp:profile'))

@login_required
def profile(request):
    return render(request, 'sakanyapp/profile.html')

#pulls route information for profile pages
@login_required
def routes(request):
    routes = UserRoute.objects.all().filter(creator=request.user)
    data = []
    for route in routes:
        route_id = route.id
        start_dt = ''
        start_time = ''
        end_dt = ''
        end_time = ''
        creation_dtg = str(route.creation_dtg)
        create_dt = route.creation_dtg.strftime('%Y/%m/%d')
        create_time = route.creation_dtg.strftime('%H:%M')

        if route.start_time:
            start_dt = route.start_time.strftime('%m/%d/%Y')
            start_time = route.start_time.strftime('%H:%M')
        if route.end_time:
            end_dt = route.end_time.strftime('%m/%d/%Y')
            end_time = route.end_time.strftime('%H:%M:%S')

        steps = RouteStep.objects.all().filter(route=route)
        routesteps = []

        for step in steps:
            open_dt = ''
            open_time = ''
            close_dt = ''
            close_time = ''
            arr_date = ''
            arr_time = ''
            if step.open_time:
                open_dt = step.open_time.strftime('%m/%d/%Y')
                open_time = step.open_time.strftime('%H:%M')
            if step.close_time:
                close_dt = step.close_time.strftime('%m/%d/%Y')
                close_time = step.close_time.strftime('%H:%M')
            if step.arr_time:
                arr_date = step.arr_time.strftime('%m/%d/%Y')
                arr_time = step.arr_time.strftime('%H:%M')
            routesteps.append({
                'order_num': step.order_num,
                'loc_name': step.loc_name,
                'loc_rating': step.loc_rating,
                'loc_address': step.loc_address,
                'loc_lat': step.loc_lat,
                'loc_lon': step.loc_lon,
                'distance': step.distance,
                'newdistance': step.newdistance,
                'unit': step.unit,
                'stars': step.stars,
                'halfstar': step.halfstar,
                'review_count': step.review_count,
                'open_dt': open_dt,
                'open_time': open_time,
                'close_dt': close_dt,
                'close_time': close_time,
                'arr_date': arr_date,
                'arr_time': arr_time,
                'visited': str(step.visited)
            })
        data.append({
            'id': route_id,
            'name': route.name,
            'creation_dtg': creation_dtg,
            'create_dt': create_dt,
            'create_time': create_time,
            'start_dt': start_dt,
            'start_time': start_time,
            'end_dt': end_dt,
            'end_time': end_time,
            'steps': routesteps
        })
        sortdata = data
        # Sorts pub routes, newest first
        data = sorted(sortdata, key=lambda i: i['creation_dtg'], reverse=True)

    # terminal testing
    for dat in data:
        print("name: " + dat['name'])
        print("start_dt / start_time: " + dat['start_dt'] + " / " + dat['start_time'])
        print("end_dt / end_time: " + dat['end_dt'] + " / " + dat['end_time'])
        for step in dat["steps"]:
            print(step)
    return JsonResponse({'routes': data})

# delete routes from profile page
@login_required
def delete_route(request, route_id):
    route = UserRoute.objects.get(id=route_id)
    route.delete()
    return HttpResponseRedirect(reverse('sakanyapp:profile'))

@login_required
def compass(request):
    # print(request.body)
    # json_data = json.loads(request.body)
    publat = request.GET["publat"]
    publon = request.GET["publon"]
    context = {
        'publat': publat,
        'publon': publon,
    }
    return render(request, 'sakanyapp/compass.html', context)
