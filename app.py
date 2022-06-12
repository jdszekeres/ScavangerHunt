URL = "https://api.geoapify.com/v2/places?categories=tourism&filter=circle:{lon},{lat},{meters}&bias=proximity:{lon},{lat}&limit={limit}&apiKey=276a11b14fef44f08a21535795486491"
from flask import *
import requests
import database
badges = [
    ("https://img.shields.io/badge/made-with-brightgreen","#","made with"),
    ("https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white","https://github.com/jdszekeres/ScavangerHunt", "github"),
    ("https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white", "https://www.postgresql.org/", "postgresql"),
    ("https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white", "https://heroku.com", "heroku"),
    ("https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white","https://code.visualstudio.com/", "visual studios code"),
    ("https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54","https://python.org", "python")
    ]
app = Flask(__name__)
app.secret_key = "\xb8\xb0spa07\x1c\xe0\xdb\xb9\xbaB\xb2\xa1\x92"
def get_lat_lon(ip):
    if ip == "127.0.0.1":
        ip = ""
    req =requests.get("http://ip-api.com/json/"+ip+"?fields=lat,lon").json()
    return req["lat"], req["lon"]
@app.route('/')
def index():
    if not "user" in session:
        return redirect("/login")
    miles = 7.5
    meters = miles*1610
    lat, lon = get_lat_lon(request.headers.get('X-Forwarded-For',request.remote_addr))
    return render_template(
        'index.html',
        stuff=requests.get(URL.format(lon=lon,lat=lat,meters=meters,limit=40)).json()["features"],
        lat=lat,
        lon=lon,
        radius=meters,badges=badges,
        points=database.get_points(session["user"])
        )
@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == "POST":
        try:
            database.create_user(request.form.get("username"), request.form.get("password"))
            session["user"] = request.form.get("username")
            return redirect("/")
        except:
            return "username exists"
    return render_template("term.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if database.validate_user(request.form.get("username"), request.form.get("password")):
            session["user"] = request.form.get("username")
            return redirect("/")
        return "The username or password you entered is invalid"
    return render_template("login.html")
@app.route("/point")
def add_point():
    if "user" in session:
        database.add_point(session["user"])
    return redirect("/?id="+request.args.get("id", "0"))
@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html",data=database.get_energy(session["user"]), board=database.get_place(session["user"]), you=session["user"])
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=1234,debug=True)