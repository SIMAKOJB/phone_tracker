import phonenumbers
import opencage
import folium
from myphone import number

from phonenumbers import geocoder

pepnumber = phonenumbers.parse(number)
location = geocoder.description_for_number(pepnumber, "en")
print(location)

from phonenumbers import carrier
service_pro = phonenumbers.parse(number)
print(carrier.name_for_number(service_pro, "en"))

from opencage.geocoder import OpenCageGeocoder

key ='b18b218fd043493ba212ace3f523a9b1'

geocoder =OpenCageGeocoder (key)
query = str(location)
results =geocoder.geocode(query)
#print(results)

lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']

print (lat,lng)

myMap = folium.map(location=[lat, lng], zoom_start=10)
folium.Marker([lat,lng], popup=location).add_to(myMap)

myMap.save("mylocation.html")