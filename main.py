def almost_main(location_user, year, file_films):
    '''The function returns sorted list by distances'''
    coordinates_list = []
    list_films = read_file(file_films)
    for i in list_films:
        if str(year) in i[0]:
            print(i[-1])
            try:
                coordinates_list.append(location(i[-1]))
            except AttributeError:
                try:
                    coordinates_list.append(location(i[-1].split(',')[1:]))
                except AttributeError:
                    coordinates_list.append(location(i[-1].split(',')[-1]))
            except GeocoderUnavailable:
                coordinates_list.append(location(i[-1].split(',')[1:]))
    distance_list = [[haversin_fopmula(i, location_user), i] for i in coordinates_list]
    return sorted(distance_list)