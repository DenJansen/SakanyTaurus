#lab26_anyapi.py

from secrets import mapapi,yelpapi #gets api keys
import requests
import json

file_path = r'results.json'

print("Pub Finder!")
print("Find the nearest pubs.")

#Get address function
def getcoords():
    #get address from user
    add1 = input("Input the house number and street name (e.g. 1600 Wabash Ave): ")
    add2 = input("Input the city: ")
    add3 = input("Input the 2-letter state: ").upper()

    #join address components to use in map url string
    streetaddress = ', '.join((add1, add2, add3))
    streetaddress = streetaddress.replace(' ', '+')

    #access api using address string and api key
    map_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={streetaddress}&key={mapapi}'
    map_response = requests.get(map_url)
    #pull coordinates
    geocoords = json.loads(map_response.text)['results'][0]['geometry']['location']

    #return latitude and longitude as a tuple
    finalcoords = (geocoords['lat'],geocoords['lng'])
    return finalcoords

#call address function to create coordinates for your address
print("Input your address:")
coords = getcoords()

yelpurl = f'https://api.yelp.com/v3/businesses/search?latitude={coords[0]}&longitude={coords[1]}&sort_by=distance&categories=breweries,brewpubs,beerbar,divebars,irish_pubs,pubs,beergarden,beergardens,barcrawl,beerhall'

# yelpurl = f'https://api.yelp.com/v3/businesses/search?latitude={coords[0]}&longitude={coords[1]}&term=hopworks'

yelpheaders = {'Authorization': 'Bearer %s' % yelpapi}
yelpresponse = requests.get(yelpurl, headers=yelpheaders)
yelpdata = json.loads(yelpresponse.text)['businesses']
with open(file_path, 'w') as file:
    file.write(yelpresponse.text)
brewerylist = []
for x in yelpdata:
    brewerylist.append((x['name'],x['location']['display_address'][0],x['location']['display_address'][-1],x['distance']))
# brewerylist.sort(key = lambda x: x[3])

if len(brewerylist) >= 10:
    total = 10
else:
    total = len(brewerylist)

print(f"\nHere are the {total} closest breweries:")
count = 0
for x in brewerylist[:total]:
    print(x[0])
    count += 1
    distance = 0.000621371 * x[3]
    distance = round(distance, 2)
    print(f"{distance} miles away")
    print(x[1])
    print(x[2] + "\n")
    if count % 3 == 0:
        input("Press ENTER to continue\n")
