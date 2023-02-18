import math
import argparse
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
import folium

parser = argparse.ArgumentParser()
parser.add_argument("year", type = int)
parser.add_argument("location1", type = float)
parser.add_argument("location2", type = float)
parser.add_argument("file", type = str)
args = parser.parse_args()

def read_file(file: str) -> list:
    '''The function reads file'''
    empty = []
    with open(file, 'r', encoding='utf-8') as new_file:
        for line in new_file:
            if line.startswith('"'):
                line = line.strip('\n').strip('\t').split('\t')
                if line[-1].startswith('('):
                    line.pop(-1)
                while '' in line:
                    line.remove('')
                empty.append(line)
    return empty
    
def haversin_fopmula(location_film: tuple, location_user: tuple) -> float:
    '''
    The function calculates distance between user and film location
    '''
    radius = 6371e3
    latitude_film = location_film[0] * math.pi / 180
    latitude_user = location_user[0] * math.pi / 180
    delta_latitude = (location_user[0] - location_film[0]) * math.pi / 180
    delta_longitude = (location_user[1] - location_film[1]) * math.pi / 180
    const_a = math.sin(delta_latitude / 2) * math.sin(delta_latitude / 2) + math.cos(latitude_film)\
    * math.cos(latitude_user) * math.sin(delta_longitude / 2) * math.sin(delta_longitude / 2)
    const_c = 2 * math.atan2(math.sqrt(const_a), math.sqrt(1 - const_a))
    return radius * const_c
    
def location(name: str) -> tuple:
    '''
    The function returns latitude and longtitude of the place
    '''
    geolocator = Nominatim(user_agent="nominatim.openstreetmap.org")
    location1 = geolocator.geocode(name)
    return (location1.latitude, location1.longitude)
