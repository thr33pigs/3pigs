#!/usr/bin/env python
# encoding: utf-8

import re
from flask import Flask,session,redirect,url_for,request,render_template,render_template_string
from func import *
from Bin import binary
from random import random
from datetime import timedelta

shop = Flask(__name__)
shop.secret_key = 'aI04\]1X.df;pOr01{];.9J"|xA1L_d-}'
b = {}

def getb(session):
    global b
    return b[session['secretkey']]

def isadmin(session):
    try:
        return 'username' in session and b[session['secretkey']]
    except:
        return False

@shop.route('/')
@shop.route('/index.php')
def index():
    if not isadmin(session):
        return redirect(url_for('login'))
    try:
        return render_template('index.html', pigs = getb(session).showpigs(), isadmin = isadmin(session))
    except:
        logout()
        return alert("Something Error")

@shop.route('/logout.php')
def logout():
    try:
        getb(session).close()
    except:
        pass
    session.clear()
    return alert("You are welcome back again!")

@shop.route('/login.php', methods=['POST', 'GET'])
def login():
    global b
    if request.method == 'GET':
        session['vcode'] = MD5(str(random()*100000000000000))[:4]
        return render_template('login.html',vcode = session['vcode'])
    elif request.method == 'POST':
        if isadmin(session):
            return redirect(url_for('index'))
        if not checklogin(request.form, session['vcode']):
            return alert("Login Failed")
        session['username'] = request.form['username']
        session['secretkey'] = int(random()*100000000000000)
        b[session['secretkey']] = binary()
        return alert("Success")

@shop.route('/manage.php', methods=['GET'])
def manage():
    if not isadmin(session):
        return alert("Not Login!")
    if request.method == 'GET':
        pigs = getb(session).getpigs()
        try:
            return render_template('manage.html', pigs = pigs[:-1], flypig = pigs[-1] , isadmin = True)
        except:
            logout()
            return alert("Time Out!")

@shop.route('/addpig.php', methods=['POST'])
def addpig():
    if not isadmin(session):
        return alert("Not Login!")
    try:
        pid = request.form.get('id','1000')[:50]
        cont = request.form.get('content',None)
        cont = cont.decode("base64")[:0xc8]
    except:
        return 'Input Error'
    if '|' in cont :
        return 'Hacker'
    ret = getb(session).addpig(pid,cont) if cont else "No Input"
    if ret == 'Time Out':
        logout()
        return ret
    else:
        return ret


@shop.route('/freepig.php', methods=['POST'])
def freepig():
    if not isadmin(session):
        return alert("Not Login!")
    try:
        pid = int(request.form.get('id','1000')[:12])
    except:
        return 'ID error'
    ret = getb(session).freepig(pid)
    if ret == 'Time Out':
        logout()
        return ret
    else:
        return ret


@shop.route('/flypig.php', methods=['POST'])
def flypig():
    if not isadmin(session):
        return alert("Not Login!")
    try:
        secret = request.form.get('secret',None)
        secret = secret.decode("base64")[:0xc0]
        useflypig = getb(session).getpigs()[-1].status
        for i in 'UOTp%I()<>S':
            if i in secret:
                return 'Hacker'
        secret = secret.format("")
    except:
        return 'Input Error'
    ret = getb(session).flypig(secret,useflypig) if secret else "No Secret"
    if ret == 'Time Out':
        logout()
        return ret
    else:
        return ret

@shop.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    shop.run(debug=True,host='0.0.0.0',port=80)

