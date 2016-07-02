import xml.etree.ElementTree as ET
import datetime as dt
from pymongo import MongoClient
import time
import pytz

gpxFile = raw_input("GPX File Name: ")

mongo = MongoClient(host="localhost")

print("Databases:\n" + str(sorted(mongo.database_names())))
db = raw_input("DB Name: ")
print("\nCollections:\n" + str(sorted(mongo[db].collection_names())))
col = raw_input("Col Name: ")

dbCol = (mongo[db])[col]

ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}

tree = ET.parse(gpxFile)
root = tree.getroot()

track = root.find("gpx:trk",ns).find("gpx:trkseg",ns)

print track

for trkpt in track.findall('gpx:trkpt',ns):
    data = trkpt.attrib
    data["ele"] = float(trkpt.find("gpx:ele",ns).text)
    timeData = dt.datetime.strptime(trkpt.find("gpx:time",ns).text, "%Y-%m-%dT%H:%M:%S.%fZ")
    timeData = pytz.utc.localize(timeData).astimezone(pytz.timezone('US/Eastern'))
    timeDataEpoch = time.mktime(timeData.timetuple())
    timeDataHuman = timeData.strftime("%Y-%m-%dT%H:%M.%S")
    
    dbCol.insert({"atype": "GPS", "vertype": 1.1, "itype": "ipad"
                    , "ts": timeDataEpoch, "hts": timeDataHuman, "param": data
                    , "comments": ["iPad GPS"], "tags": ["iPad", "gps"]})