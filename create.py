import sqlite3

db=sqlite3.connect('data.db')
cur=db.cursor()

cur.execute('create table userinfo(name varchar(50) ,password varchar(50))')
cur.execute('create table chart(name varchar(50),speed text,score integer,time text)')
cur.execute('insert into userinfo(name,password) values(?,?)',['admin','123456'])
cur.execute('insert into chart(name,speed,score,time) values(?,?,?,?)',['admin','Fast',99999,'2023-04-30 01:04:54'])

db.commit()
cur.close()
db.close()