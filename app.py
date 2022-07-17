URL = "https://api.geoapify.com/v2/places?categories=entertainment,leisure,natural,national_park,pet.dog_park,tourism,beach,heritage,public_transport,ski,sport.stadium,building.historic,building.tourism,building.entertainment,activity&filter=circle:{lon},{lat},{meters}&bias=proximity:{lon},{lat}&limit={limit}&apiKey={key}"
from flask import *
from flask_compress import Compress
import requests
import database 
from random import choice
import urllib3
import math
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371000  # meters

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d
badges = [
    ("https://www.scouting.org/wp-content/uploads/2019/09/merit-badge-GameDesign.svg","#","for the game design merit badge")
    # ("https://img.shields.io/badge/made-with-brightgreen","#","made with"),
    # ("https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white","https://github.com/jdszekeres/ScavangerHunt", "github"),
    # ("https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white", "https://www.postgresql.org/", "postgresql"),
    # ("https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white", "https://heroku.com", "heroku"),
    # ("https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white","https://code.visualstudio.com/", "visual studios code"),
    # ("https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54","https://python.org", "python")
    ]
urls=[
    "https://api.mapbox.com/styles/v1/yopo/cl3yq1zr3000014oaaez3upb0/tiles/512/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoieW9wbyIsImEiOiJjbDA0bzhoM2EwMWhiM2NxajV2Zm1lYmpyIn0.kL4KlQH8tl89C6dJtL31gw",
    "https://api.mapbox.com/styles/v1/puggle-wuggle/cl4eig5ow000115oxhw88uiem/tiles/512/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoicHVnZ2xlLXd1Z2dsZSIsImEiOiJjbDRlaWVzMmswM3k5M2VsaWNpc2V3MGQ4In0.SC8EX6RjDonfDF8yo2Wjdw"
    ]
keys=[
    "6676411bb88844ae92b0e1bbde4f0652",
    "276a11b14fef44f08a21535795486491"
]
key=choice(keys)
app = Flask(__name__)
Compress(app)
app.secret_key = "\xb8\xb0spa07\x1c\xe0\xdb\xb9\xbaB\xb2\xa1\x92"
def get_place(user,board):
    for i,v in enumerate(board):
        if user==v[1]:
            return i+1
def find_nearest(point, points):
    closest = 1234567890
    for i in points:
        if i != point:
            d=distance(point, i)
            if d<closest:
                closest=d
        else:
            print("duplicate:"+str(i)+"\n")
    return closest
                
app.jinja_env.globals.update(place=get_place)
app.jinja_env.globals.update(enumerate=enumerate)
app.jinja_env.globals.update(round=round)
app.jinja_env.globals.update(find_nearest=find_nearest)
@app.after_request
def enforce_https(response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    return response
def get_lat_lon(ip):
    if ip == "127.0.0.1":
        ip = ""
    req =requests.get("http://ip-api.com/json/"+ip+"?fields=lat,lon", verify=False).json()
    return req["lat"], req["lon"]

@app.route('/')
def index():
    if not "user" in session:
        return redirect("/login")
    miles = 10
    meters = miles*1610
    limit=200
    lat, lon = get_lat_lon(request.headers.get('X-Forwarded-For',request.remote_addr))
    if "location" in session:
        lat = session["location"]["lat"]
        lon = session["location"]["lon"]
    features=requests.get(URL.format(lon=lon,lat=lat,meters=meters,limit=limit,key=key), verify=False).json()["features"]
    print(lat,lon)
    temp = make_response(render_template(
        'index.html',
        stuff=features,
        lat=lat,
        lon=lon,
        radius=meters,
        badges=badges,
        points=database.get_points(session["user"]),
        tip="",
        url=choice(urls)
        ))
    temp.headers.set("Content-Security-Policy","script-src 'nonce-1f40e4a23493'")
    return temp
@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == "POST":
        try:
            database.create_user(request.form.get("username"), request.form.get("password"))
            session.permanent = True
            session["user"] = request.form.get("username")
            return redirect("/")
        except Exception as e:
            return "username exists: "+str(e)
    keywords = ['Mobile','Opera Mini','Android', 'Iphone', "Ipad"]
    user_agent = request.headers.get('User-Agent').lower()
    if any(word.lower() in user_agent for word in keywords):
        return render_template("simple_signup.html")
    else:
        return render_template("term.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if database.validate_user(request.form.get("username"), request.form.get("password")):
            session.permanent = True
            session["user"] = request.form.get("username")
            return redirect("/")
        return "The username or password you entered is invalid"
    return render_template("login.html")
@app.route("/point")
def add_point():
    if "user" in session:
        database.add_point(session["user"])
    return """<meta http-equiv="refresh" content="0;URL='https://game-design-mb.herokuapp.com/?id={}&name={}'" />""".format(request.args.get("id", "0"),request.args.get("name","0"))
@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html",data=database.get_energy(session["user"]), board=database.get_place(session["user"]), you=session["user"])
@app.route("/update", methods=["POST"])
def update_location():
    print(request.json)
    if "lat" in request.json:
        session["location"] = request.json
    return jsonify(request.json)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=1234,debug=True,threaded=True)