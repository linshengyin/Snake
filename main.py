from flask import Flask,render_template,redirect,request
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField
from flask_bootstrap import Bootstrap
from itertools import chain
import sqlite3,datetime

class fform(FlaskForm):
    usn=StringField("username")
    psw=StringField("password")
    su=SubmitField('提交')

DATABASE='data.db'
app=Flask(__name__)
bootstrap=Bootstrap(app)
app.config['SECRET_KEY']="SECRET_KEY"
un,speed,flag='','Medium',False
spdic={'Fast':'2','Medium':'1','Slow':'0'}

@app.route('/')
def ma():
    global un,flag
    un,flag='',False
    return render_template('main.html')

@app.route('/input',methods=['GET'])
def insert():
    global un,speed
    score=int(request.args.get('score'))
    nowtime=datetime.datetime.now()
    nowtime=nowtime.strftime('%Y-%m-%d %H:%M:%S')
    db=sqlite3.connect(DATABASE)
    cur=db.cursor()
    cur.execute('select * from chart where name = ?',[un])
    da=cur.fetchall()
    da=list(chain.from_iterable(da))
    if da==[]:
        cur.execute('insert into chart(name,speed,score,time) values(?,?,?,?)',[un,speed,score,nowtime])
        db.commit()
    elif spdic[da[1]]<spdic[speed] and da[2]==score or da[2]<score:
        cur.execute('update chart set speed = ?,score = ?,time = ? where name = ?',[speed,score,nowtime,un])
        db.commit()
    cur.close()
    db.close()

@app.route('/ifgame',methods=['GET'])
def ifga():
    global flag,speed
    if flag:
        return ['1',speed]
    else:
        return ['0']

@app.route('/log',methods=["GET","POST"])
def lo():
    global un,flag
    no,un,flag='','',False
    ff=fform()
    if ff.validate_on_submit():
        usn=ff.usn.data
        psw=ff.psw.data
        db=sqlite3.connect(DATABASE)
        cur=db.cursor()
        cur.execute('select * from userinfo where name = ?',[usn])
        da=cur.fetchall()
        cur.close()
        db.close()
        da=list(chain.from_iterable(da))
        if da!=[] and da[1]==psw:
            un=usn
            return redirect('/game')
        else:
            no='用户名或密码错误'
    return render_template('log.html',form=ff,no=no)

@app.route('/reg',methods=["GET","POST"])
def re():
    global un,flag
    no,un,flag='','',False
    ff=fform()
    if ff.validate_on_submit():
        usn=ff.usn.data
        psw=ff.psw.data
        db=sqlite3.connect(DATABASE)
        cur=db.cursor()
        cursor=cur.execute('select * from userinfo where name = ?',[usn])
        if len(list(cursor))==0:
            cur.execute('insert into userinfo(name,password) values(?,?)',[usn,psw])
            db.commit()
            cur.close()
            db.close()
            un=usn
            return redirect('/game')
        else:
            no='该用户名已存在'
            cur.close()
            db.close()
    return render_template('reg.html',form=ff,no=no)

@app.route('/set',methods=["GET","POST"])
def se():
    global speed
    sped=request.form.get('option')
    if sped=='Fast' or sped=='Slow':
        speed=sped
    else:
        speed='Medium'
    options=['Fast','Medium','Slow']
    return render_template('set.html',options=options)

@app.route('/cha',methods=['GET','POST'])
def ch():
    db=sqlite3.connect(DATABASE)
    cur=db.cursor()
    cur.execute('select * from chart order by score desc,speed asc')
    data=cur.fetchall()
    cur.close()
    db.close()
    return render_template('cha.html', data=data)

@app.route('/game',methods=['GET','POST'])
def ga():
    global un,flag
    flag=True
    if un=='':
        return redirect('/')
    else:
        no='ENJOY YOUR GAME! '+un
        return render_template('game.html', no=no)
    
app.run(host='10.0.0.23',port=7999,debug=True)