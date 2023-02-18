def location(name: str) -> tuple:
    '''
    The function returns latitude and longtitude of the place
    '''
    geolocator = Nominatim(user_agent="nominatim.openstreetmap.org")
    location1 = geolocator.geocode(name)
    return (location1.latitude, location1.longitude)