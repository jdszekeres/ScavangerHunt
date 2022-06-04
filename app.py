URL = "https://api.geoapify.com/v2/places?categories=tourism&filter=circle:{lon},{lat},{meters}&bias=proximity:{lon},{lat}&limit={limit}&apiKey=276a11b14fef44f08a21535795486491"
from flask import *
import requests
app = Flask(__name__)
def get_lat_lon(ip):
    if ip == "127.0.0.1":
        ip = ""
    req =requests.get("http://ip-api.com/json/"+ip+"?fields=lat,lon").json()
    return req["lat"], req["lon"]
@app.route('/')
def index():
    miles = 5
    meters = miles*1610
    lat, lon = get_lat_lon("127.0.0.1")
    return render_template('index.html', stuff =  requests.get(URL.format(lon=lon,lat=lat,meters=meters,limit=50)).json()["features"], lat=lat,lon=lon, radius=meters)
app.run(debug=True)