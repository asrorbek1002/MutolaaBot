from geopy.geocoders import Nominatim

def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="tgBot")
    location = geolocator.reverse(f"{latitude}, {longitude}")
    print(location)
    return location.address