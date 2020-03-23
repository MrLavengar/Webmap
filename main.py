from pandas import read_csv, read_excel
from folium import Map, FeatureGroup, IFrame, Popup, CircleMarker, Marker, LayerControl
from numpy import nan_to_num, isnan

map = Map(location=[31, 20], zoom_start=3, tiles="Stamen Terrain")


def add_volcanoes(map):
    map = map
    volcanoes = read_excel('volcanoes.xlsx').iloc[1:, [1, 2, 4, 5, 6]]
    latitudes, longitudes = volcanoes['Latitude'], volcanoes['Longitude']
    name = volcanoes['Volcano Name']
    country = volcanoes['Country']
    elevation = volcanoes['Elev']

    fg_volcanoes = FeatureGroup(name='Volcanoes', show=False)

    def color_by_elevation(elev):
        if type(elev) == str:
            return 'white'
        if elev <= -4000:
            return 'darkblue'
        if elev <= -2000:
            return 'cadetblue'
        if elev <= 0:
            return 'lightblue'
        if elev <= 2000:
            return 'orange'
        if elev <= 4000:
            return 'red'
        if elev <= 6000:
            return 'darkred'
        else:
            return 'black'

    for i in range(len(volcanoes)):
        i += 1
        if isnan(elevation[i]):
            elevation[i] = 'Unknown'
        if name[i] == 'Unnamed':
            html = f'Volcano name:{name[i]}<br>Height: {elevation[i]} m<br> {country[i]}'
        else:
            html = f'Volcano name:<b4> <a href="https://www.google.com/search?q={name[i]} volcano" target="_blank">{name[i]}</a><br> \
                Height: {elevation[i]} m<br> {country[i]}'

        iframe = IFrame(html=html, width=200, height=100)
        coords = (latitudes[i], longitudes[i])
        fg_volcanoes.add_child(CircleMarker(location=coords, popup=Popup(iframe), color="gry",
                                            fill_color=color_by_elevation(elevation[i]), fill_opacity=0.9, radius=6))
        i -= 1

    map.add_child(fg_volcanoes)


def add_cities(map):
    cities = read_csv('worldcities.csv').iloc[:, [1, 2, 3, 4, 7, 8, 9]]
    latitudes, longitiudes = cities['lat'], cities['lng']
    name = cities['city_ascii']
    country = cities['country']
    admin_name = cities['admin_name']
    population = cities['population']

    fg_05to1m_cities = FeatureGroup(name='500k-1m', show=False)
    fg_1to2m_cities = FeatureGroup(name='1m-2m', show=False)
    fg_2to5m_cities = FeatureGroup(name='2m-5m', show=False)
    fg_5to10m_cities = FeatureGroup(name='5m-10m', show=False)
    fg_more_than_10m_cities = FeatureGroup(name='>10m', show=False)

    for i in range(len(cities)):
        if nan_to_num(population[i]) < 500000:
            continue
        html = f'City: <a href="https://www.google.com/search?q={name[i]} city" target="_blank">{name[i]}</a><br> \
                        Admin: {admin_name[i]}<br> \
                        Country: {country[i]}<br>\
                        Population: {population[i]}'
        iframe = IFrame(html=html, width=200, height=200)
        coords = (latitudes[i], longitiudes[i])

        if population[i] < 1000000:
            fg_05to1m_cities.add_child(Marker(location=coords, popup=Popup(iframe)))
        elif population[i] < 2000000:
            fg_1to2m_cities.add_child(Marker(location=coords, popup=Popup(iframe)))
        elif population[i] < 5000000:
            fg_2to5m_cities.add_child(Marker(location=coords, popup=Popup(iframe)))
        elif population[i] < 10000000:
            fg_5to10m_cities.add_child(Marker(location=coords, popup=Popup(iframe)))
        elif population[i] >= 1000000:
            fg_more_than_10m_cities.add_child(Marker(location=coords, popup=Popup(iframe)))

    map.add_child(fg_05to1m_cities)
    map.add_child(fg_1to2m_cities)
    map.add_child(fg_2to5m_cities)
    map.add_child(fg_5to10m_cities)
    map.add_child(fg_more_than_10m_cities)


add_volcanoes(map)
add_cities(map)
map.add_child(LayerControl())
map.save('Map1.html')
