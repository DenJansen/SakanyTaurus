# Name
## Sakany Taurus
### A Pub Crawler

# Project Overview
## Summary
The purpose of this application is to create pub crawl routes, in which the user is able to identify pubs/breweries/bars in their area, select the locations they want to visit, and generate a walking route for a pub crawl with their friends. The application will also incorporate a virtual compass that will point to the next pub along the user's route.
## Libraries/Frameworks
This application will use the Google Maps and Yelp APIs to locate pubs and plot routes on the map. Graphical interface will use the Pure CSS framework. The compass will be designed using [lamplightdev's HTML5 code](https://github.com/lamplightdev/compass).

# Functionality
This site will be designed with a mobile-first approach, particularly in consideration of the compass functionality.
## Login Page
The user will first be faced with a login/registration page, which will include a couple screenshots demonstrating the web application. As a stretch goal, there will be a link to a demo page where they can test out the functionality without logging in.
## Route Builder Page
After logging in, this page will display the features for creating the user's route if they have not previously created one. Otherwise, they will load to the display route page (see below). As a stretch goal, the user will be able to save more than one route at a time.

The route builder will start with a search box where the user can input an address or set of coordinates (stretch goal: prompt for user's current location, and allow the user to optionally provide a start/stop time for the pub crawl to determine if locations will be open). This information will be sent to the Yelp API on the back-end, where it will return the nearest 25 results and display them on a map using the Google Maps API. It will also display the results as a clickable list where the user can click and select the locations to add to their route (stretch goal: user can click directly on the map icons to add to route). The location information will include distance, rating, location type (brewpub, bar, etc), and open hours (if available) from the Yelp API.

## Display Route Page
After submitting their selections, this information will be stored on the back-end as a list tied to the currently logged in user. The app will display their route and calculate the total travel time and distance between pubs (stretch goal: the app will calculate this as the user adds locations to their route). From here, the user can remove locations from the route. As a stretch goal, the user profile can store more than one route at a time.

The user will be able to "Start crawl" from here, at which point the app will start the user on their route. As a stretch goal, the page will adjust the route depending on if locations have closed.
As the user visits locations, they can mark it off as visited on this page, which will be sent to the back-end as a boolean stored with the route list. For the currently active location, the user can click on a "Compass" button to go to the compass mode for navigation to the next pub.

## Compass Page
This page will provide an as-the-crow-flies compass which will point to the next pub. As a stretch goal, there will be an optional navigation button that sends the user to google maps if they prefer specific navigation instructions.

# Data Model
## user
A database of registered users

## user_route
Stores the user's current route

## favorites
Stretch goal: allows user to store favorite locations for future pub crawls

# Schedule
## Phase One
Create user login, route builder, and display route pages - 1-2 weeks

## Phase Two
Create compass page - 2-3 days

## Phase Three
Start on stretch goals:
- Start/stop time check of pub hours when creating route
- "Start crawl" feature
- User location prompt
- Recalculate route if locations closed based on current time when "start crawl" feature active
- Minimum password requirements tester
- Save user's favorite locations

## Phase Four
Work on additional stretch goals:
- Create Demo Page as single-page javascript that does not store information on the back-end
- Calculate route time as user adds locations
- Multiple route functionality
- Clickable map icons to add to route
- Navigation button to send compass location to Google Maps
