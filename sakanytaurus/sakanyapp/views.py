from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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

def login_page(request):
    message = request.GET.get('message', '')
    next = request.GET.get('next', '')
    context = {
        'next': next,
        'message': message
    }
    return render(request, 'sakanyapp/login.html', context)

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

@login_required
def index(request):
    context = {
        'mapapi': secrets.mapapi
    }
    return render(request, 'sakanyapp/index.html', context)

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

    # pubresults = {}
    # for x in yelpdata:
    #     pubresults.append((x['name'],x['location']['display_address'][0],x['location']['display_address'][-1],x['distance']))
    #
    # print(pubresults)
    # counter = 0
    # for i in yelpdata:
    #     key = str(counter)
    #     pubresults[key] = i
    #     counter += 1
    #
    # print(pubresults)
    #
    # return HttpResponse("Success!")

    return JsonResponse({'pubresults':yelpdata,'origin':origin})

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
        create_crawl = RouteStep(route=newcrawl, order_num=order_num, loc_name=loc_name, loc_rating=loc_rating, loc_address=loc_address, loc_lat=loc_lat, loc_lon=loc_lon)
        create_crawl.save()

    return HttpResponseRedirect(reverse('sakanyapp:profile'))

@login_required
def profile(request):
    routes = UserRoute.objects.all().filter(creator=request.user)
    context = {
        'routes': routes
    }
    return render(request, 'sakanyapp/profile.html', context)
