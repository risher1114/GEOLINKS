import json
import math
import urllib2

from xlrd import open_workbook

# Automatically geolocate the connecting IP
f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)
#print(location)

longi = location['longitude']
lati = location ['latitude']
###print lati
## finding the diffrence in latitude and longitude between two points to
## determine the closest stream guage location to find the real time
## stream data
mindis=10000
minlat = 80
minlong =0
minstation = 0
minflood = 0

book = open_workbook("C://Temp/latlongtable2.xls")
#book = open_workbook("/Users/upendragiri/Desktop/latlongtable.xls")


sheet = book.sheet_by_index(0)
for i in range(1, sheet.nrows):
    row = sheet.row_values(i)
    variable1 = row[14]
    variable2 = row[15]
    stationid = row[5]
    floodstage = row[20]
    ##print (variable2)
    ##variable1,variable2 = map(math.radians,[variable1,variable2])

# approximate radius of earth in km
    R = 6373.0
    lat1 = (variable1)          
    lon1 = (variable2)
    lat2 =  lati                     
    lon2 =  longi                      
    staid = stationid
    floid = floodstage
   

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    if (d < mindis):
        mindis = d
        minlat = lat1
        minlong = lon1
        minstation = staid
        minflood = floid
        
#    print d
#print mindis + lat1 +" long" + lon1
##print mindis
print minlat
print minlong

#print minstation
#print str(minflood) + ("      flooding value ")
### retreving data from the stream guage station.
import urllib2, json

url='http://waterservices.usgs.gov/nwis/iv/?format=json&sites='+minstation+'&parameterCd=00060,00065&siteStatus=all'
req=urllib2.Request(url)
opener=urllib2.build_opener()
f=opener.open(req)
entry=json.loads(f.read())
#print (entry)
count=int(len(entry['value']['timeSeries'])-1)
while count>=0:
    gauge=entry['value']['timeSeries'][count]['values'][0]['value'][0]['value']
    print str(gauge) + ("       gauge reading")    
    break
    count+=1
##    if gauge>minflood:
##        print"flooding"
##    else:
##        print"no flood"
##print gauge
##print minflood

gauge1=6
minflood1= 8
##if gauge1<minflood1:
if gauge<minflood:
    print"flooding"
else:
    print"no flood"


import urllib2, json
url='https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key=AIzaSyA2L7UAX8CW6tmlparkTTYft2mE5rIWMOo'
req=urllib2.Request(url)
opener=urllib2.build_opener()
f=opener.open(req)
#entry=json.load(f.read())
entry=json.loads(f.read())
#print entry
elevation= entry['results'][0]['elevation']
print elevation

#Plotting coordinates in google map
import os
import webbrowser
lat2 = minlat
lng2 = minlong
file = open("C:/Users/wuxia/Desktop/AdGIS_project/newmypage.html","w")
    
file.write("""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">
  html { height: 100% }
  body { height: 100%; margin: 0; padding: 0 }
  #map_canvas { height: 100% }
</style>
<script type="text/javascript"
    src="http://maps.googleapis.com/maps/api/js?sensor=true">
</script>
<script type="text/javascript">
  function initialize() {
    var myLatLng = new google.maps.LatLng(34.7495002747,-86.6252975464);
    var myOptions = {
      zoom: 8,
      center: myLatLng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var myMap = new google.maps.Map(document.getElementById("map_canvas"),
        myOptions);
 
    var myLatLng = new google.maps.LatLng(34.7495002747,-86.6252975464);
    var myMarkerOptions = {
	position: myLatLng,
	map: myMap,
	title: 'My marker for lab 10',
	clickable: true
    }
    var marker = new google.maps.Marker(myMarkerOptions);
  }

</script>
</head>
<body onload="initialize()">
  <div id="map_canvas" style="width:100%; height:100%"></div>
</body>
</html>
""")
file.close()



    
###view newmapge.html on goooglemap
import webbrowser
f=open("C:/Users/wuxia/Desktop/AdGIS_project/newmypage.html","r")
filename="C:/Users/wuxia/Desktop/AdGIS_project/mypage.html/"
webbrowser.open_new_tab("C:/Users/wuxia/Desktop/AdGIS_project/newmypage.html")



    
   
