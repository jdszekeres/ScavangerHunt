url = "postgres://wxvjdiftesdjlv:a0a5e931304fb58d774c2ab7e42bbbb5840337d0192335be1993c49b1ba99635@ec2-54-165-178-178.compute-1.amazonaws.com:5432/d2dgk4gg48g0gr"
import psycopg2
import os
def cc():
    """create con and cur"""
    conn = psycopg2.connect(url)
    return conn, conn.cursor()
con,cur = cc()
cur.execute("CREATE TABLE IF NOT EXISTS users (id serial primary key, username text, password text, points int);")
con.commit()
if __name__ == "__main__":
    os.system("pgweb --url '{}'".format(url))