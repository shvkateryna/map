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