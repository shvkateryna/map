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