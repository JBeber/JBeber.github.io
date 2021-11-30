import folium

# custom coordinates
COORDS = {'Home'              : [38.03048298602479, -84.49403102718946],
          'Morgan'            : [38.03580964983726, -84.50849973222947],
          'Student Center'    : [38.03985341206333, -84.50296869770293],
          'Alumni Gym'        : [38.04069980883591, -84.5035298155715],
          'CCI'               : [38.029920646644364, -84.49042064562035],
          'Bear & the Butcher': [38.03023333251369, -84.4907317818482],
          'Charlie Brown\'s'  : [38.02986791634865, -84.49101061344437]}


# create base map and specify center point, zoom settings, and terrain tiles
map = folium.Map(location=COORDS['Student Center'], max_zoom=20, zoom_start=15.5)

# create a feature group for each layer of features to add to the map
markers = folium.FeatureGroup(name="Markers")

# custom popup html
html = """
<center>%s</center>
"""

# create markers and add to the feature group
for label in COORDS:
    iframe = folium.IFrame(html= html % label, width=150, height=55)
    markers.add_child(folium.Marker(COORDS[label], popup=folium.Popup(iframe), icon=folium.Icon(color='blue')))

# add feature groups to the map
map.add_child(markers)

# save map to file
map.save("custom_map.html")