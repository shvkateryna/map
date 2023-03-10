"""Functions about films and locations"""
import math
import argparse
from geopy.extra.rate_limiter import RateLimiter
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

print(read_file('location2.list'))
def haversin_fopmula(location_film: tuple, location_user: tuple) -> float:
    '''
    The function calculates distance between user and film location
    >>> haversin_formula((35.1460249, -90.0517638), (49.163168, -123.137414))
    3105600.0423169667
    >>> haversin_fopmula((-22.9997404, -43.3659929), (34.0536909, -118.242766))
    10133840.565664798
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
    >>> location('Новий Яричів')
    (49.9071883, 24.3026191)
    >>> location('Los Angeles')
    (34.0536909, -118.242766)
    '''
    geolocator = Nominatim(user_agent="nominatim.openstreetmap.org")
    location1 = geolocator.geocode(name)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    return (location1.latitude, location1.longitude)

def almost_main(location_user, year, file_films):
    '''The function returns sorted list by distances'''
    coordinates_list = []
    list_films = read_file(file_films)
    for i in list_films:
        if str(year) in i[0]:
            print(i[-1])
            try:
                coordinates_list.append(location(i[-1]))
            except (AttributeError, GeocoderUnavailable):
                try:
                    coordinates_list.append(location(i[-1].split(',')[1:]))
                except (AttributeError, GeocoderUnavailable):
                    coordinates_list.append(location(i[-1].split(',')[-1]))
    distance_list = [[haversin_fopmula(i, location_user), i] for i in coordinates_list]
    return sorted(distance_list)

def map_creator(year, location_user, file_films):
    '''The function creates the map'''
    my_map = folium.Map()
    html = """<h4>{} рік</h4>
    Кількість знятих фільмів: {}
    """
    figure = folium.FeatureGroup(name = 'films locations')
    figure2 = folium.FeatureGroup(name = 'the closest location')
    distance_list = almost_main(location_user, year, file_films)
    last_list = []
    for  element in distance_list:
        if distance_list.count(element) == 1:
            last_list.append([element, 1])
        else:
            if [element, distance_list.count(element)] not in last_list:
                last_list.append([element, distance_list.count(element)])
    markers_counter = 0

    if len(last_list) >= 10:
        last_list = last_list[:10]

    for markers_counter, _ in enumerate(last_list):
        figure2.add_child(folium.CircleMarker(location = [last_list[0][0][1][0], last_list[0][0][1][1]],
                                      radius=10,
                                      popup='the closest location',
                                      fill_color = 'red',
                                      color = 'green',
                                      fill_opacity=0.5))
        iframe = folium.IFrame(html=html.format(year, last_list[markers_counter][1]),
                          width=300,
                          height=100)

        figure.add_child(folium.Marker(location=[last_list[markers_counter][0][1][0],
                last_list[markers_counter][0][1][1]],
                popup=folium.Popup(iframe),
                icon=folium.Icon(color = "green", icon = "fa-thin fa-camera-retro", prefix = 'fa')))
        my_map.add_child(figure)
        my_map.add_child(figure2)
    my_map.add_child(folium.LayerControl())
    my_map.save('map.html')

map_creator(args.year, (args.location1, args.location2), args.file)

