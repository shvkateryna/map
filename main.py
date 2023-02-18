def map_creator(year, location_user, file_films):
    '''The function creates the map'''
    my_map = folium.Map()
    html = """<h4>{} рік</h4>
    Кількість знятих фільмів: {}
    """
    figure = folium.FeatureGroup()
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

    for markers_counter, element in enumerate(last_list):
        iframe = folium.IFrame(html=html.format(year, last_list[markers_counter][1]),
                          width=300,
                          height=100)

        figure.add_child(folium.Marker(location=[last_list[markers_counter][0][1][0],
                last_list[markers_counter][0][1][1]],
                popup=folium.Popup(iframe),
                icon=folium.Icon(color = "green", icon = "fa-thin fa-camera-retro", prefix = 'fa')))

        if markers_counter == len(last_list) - 1:
            break
        markers_counter += 1
        my_map.add_child(figure)
    my_map.save('map.html')