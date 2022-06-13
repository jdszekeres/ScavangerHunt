url = "postgres://wxvjdiftesdjlv:a0a5e931304fb58d774c2ab7e42bbbb5840337d0192335be1993c49b1ba99635@ec2-54-165-178-178.compute-1.amazonaws.com:5432/d2dgk4gg48g0gr"
WATTS_PER_HOUR = 1.239
import psycopg2
import os
from operator import itemgetter
def cc():
    """create con and cur"""
    conn = psycopg2.connect(url)
    return conn, conn.cursor()
con,cur = cc()
cur.execute("CREATE TABLE IF NOT EXISTS users (id serial primary key, username text, password text, points int);")
con.commit()
def create_user(name, password):
    conn,cur = cc()
    cur.execute("SELECT * from users WHERE username = '{}'".format(name))
    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO users (username,password,points) VALUES ('{}','{}',0);".format(name, password))
        conn.commit()
    else:
        raise Exception("user exists")
def validate_user(username,password):
    conn,cur = cc()
    cur.execute("SELECT * FROM users WHERE username = '{}' and password = '{}'".format(username, password))
    return len(cur.fetchall()) != 0
def add_point(username):
    conn,cur = cc()
    cur.execute("SELECT points FROM users where username = '{}'".format(username))
    new_points = int(cur.fetchall()[0][0])+1
    print("New points for {}: {}".format(username, new_points))
    cur.execute("update users set points = '{}' where username = '{}'".format(new_points, username))
    conn.commit()
def get_points(username):
    conn,cur = cc()
    cur.execute("SELECT points FROM users where username = '{}'".format(username))
    return int(cur.fetchall()[0][0])
def get_energy(username):
    conn, cur = cc()
    cur.execute("SELECT points FROM users")
    total = 0
    for i in cur.fetchall():
        total += i[0]
    cur.execute("SELECT points FROM users WHERE username = '{}'".format(username))
    self_points = cur.fetchall()[0][0]
    return {"total":total,"self":self_points,"percent":(self_points/total)*100,"wh":WATTS_PER_HOUR}
def get_place(username):
    conn, cur = cc()
    cur.execute("SELECT points, username FROM users")
    list_of_users = sorted(cur.fetchall(), key=lambda x: x[0])[::-1]
    return list_of_users
if __name__ == "__main__":
    os.system("pgweb --url '{}'".format(url))