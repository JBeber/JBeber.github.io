import pandas as pd
import folium

data = pd.read_csv("Volcanoes.txt")

# create lists of data for each marker (these can be read faster than pandas Series)
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

# custom popup html
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s volcano%%22" target="_blank">%s</a><br><br>
Height: %s m
"""

# dynamic popup color determination
def get_popup_color(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

# create base map and specify center point, zoom settings, and terrain tiles
map = folium.Map(location=[lat[0],lon[0]], max_zoom=20, zoom_start=10)

# create a feature group for each layer of features to add to the map
markers = folium.FeatureGroup(name="Markers")

polygons = folium.FeatureGroup(name="Population Polygons")

# create markers and add to the feature group
for lt, ln, el, nm in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (nm, nm, el), width=200, height=100)
    markers.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(iframe), fill_color=get_popup_color(el), fill_opacity=0.7, color='grey', zIndexOffset=1000))

# use Folium's GeoJson module to add polygon data to the map
# set fill_color depending on population
polygons.add_child(folium.GeoJson(data=(open("world.json", 'r', encoding='utf-8-sig').read()),
                                     style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 1000000
                                                              else 'orange' if 1000000 <= x['properties']['POP2005'] < 20000000
                                                              else 'red'}))

# add feature groups to the map
map.add_child(markers)
map.add_child(polygons)

# add a layer control interface
'''NOTE this must be added AFTER the other layers'''
map.add_child(folium.LayerControl())

# save map to file
map.save("volcanoes.html")