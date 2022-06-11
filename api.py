# coding=utf-8
import sqlite3,datetime
from atexit import register as registerExit
from flask import Flask,request,jsonify
from re import compile as re_compile
from os import mkdir
from os import name as osname
from json import loads
# Database
from hashlib import sha256
from os.path import exists
from random import randint
from os import popen
from platform import platform
# project: GitHub Tools Feedback Serve API Core
# file: api.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: LTS(Long Term Support) 1.0.1
# Publish only on GitHub
# Copyright 2022 MacWinLin Studio.All rights reserved.

# Code

def genRandomString(lenA=1,lenB=5):
    String = ''
    for i in range(randint(lenA,lenB)):
        StringType = randint(1,3)
        # 0-9
        if StringType == 0:
            StringUnicode = randint(48,57)
        # A-Z
        elif StringType == 1:
            StringUnicode = randint(65,90)
        # a-z
        else:
            StringUnicode = randint(97,122)
        # Unicode --> String
        String += chr(StringUnicode)
    return String
def createDatabase():
    con = sqlite3.connect('.mwl-githut-fb-data.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS basicData(id INTEGER PRIMARY KEY,register INTEGER NOT NULL DEFAULT 0,registerOrganization INTEGER NOT NULL DEFAULT 0,domain TEXT NOT NULL DEFAULT 'http://127.0.0.1:5000',autoGenJson INTEGER NOT NULL DEFAULT 1,ipv4 INTEGER NOT NULL DEFAULT 1,ipv6 INTEGER NOT NULL DEFAULT 0)")
    cur.execute("INSERT INTO basicData VALUES (1,0,0,'http://127.0.0.1:5000',1,1,0)")
    cur.execute("CREATE TABLE IF NOT EXISTS account(email TEXT NOT NULL,pwd TEXT NOT NULL,userLevel INTEGER NOT NULL DEFAULT 0,block INTEGER NOT NULL DEFAULT 0,userType INTEGER NOT NULL DEFAULT 0)")
    randomPassword = genRandomString()
    randomPasswordSHA256 = sha256(randomPassword.encode()).hexdigest()
    cur.execute("INSERT INTO account VALUES ('root','{}',2,0,0)".format(randomPasswordSHA256))
    con.commit()
    cur.close()
    con.close()
    # Windows System Hidden Database
    if 'Windows' in platform():
        popen('attrib +H .mwl-githut-fb-data.db')
    return randomPassword
# Check database
if not exists('.mwl-githut-fb-data.db'):
    print('ROOT Password:{},won\'t show again!'.format(createDatabase()))

# Really code

enableRegister = None
enableRegisterOrganization = None
def verifyEmail(email):
    ex_email = re_compile(r'^[\w][a-zA-Z1-9.]{4,19}@[a-zA-Z0-9]{2,3}.[com|gov|net]')
    result = ex_email.match(email)
    if result:
        return True
    else:
        return False
def start(register,registerOrganization):
    global enableRegister
    global enableRegisterOrganization
    if register == 0:
        enableRegister = True
    else:
        enableRegister = False
    if registerOrganization == 0:
        enableRegisterOrganization = True
    else:
        enableRegisterOrganization = False
    con = sqlite3.connect('.mwl-githut-fb-data.db')
    cur = con.cursor()
    cur.execute('select * from basicData')
    cache = cur.fetchone()
    cur.close()
    con.close()
    if cache[4] == 1:
        mkdir('feedback')
        if osname == 'nt':
            jsonFile = open(r'feedback\feedback.json','w')
        else:
            jsonFile = open('feedback/feedback.json','w')
        if cache[5] == 0:
            ipv4 = 'false'
        else:
            ipv4 = 'true'
        if cache[6] == 0:
            ipv6 = 'false'
        else:
            ipv6 = 'true'
        jsonFile.write('"enabled":true,"ipv4":{},"ipv6":{},"link":"{}"'.format(ipv4,ipv6,cache[3]))
        jsonFile.close()
        if osname == 'nt':
            jsonFile = open(r'feedback\feedback-organization.json','w')
        else:
            jsonFile = open('feedback/feedback-organization.json','w')
        jsonFile.write('"enabled":true,"ipv4":{},"ipv6":{},"link::"{}"'.format(ipv4,ipv6,cache[3]))
        jsonFile.close()
app = Flask(__name__)
file = open('feedbacks.txt','a')
now = datetime.datetime.now()
@app.route('/login/',methods=['POST'])
def login():
    email = request.json.get('account').strip()
    pwd = request.json.get('password').strip()
    con = sqlite3.connect('.mwl-githut-fb-data.db')
    cur = con.cursor()
    cur.execute('SELECT email FROM account')
    sqlData = cur.fetchall()
    sqlDataCache = []
    for i in range(len(sqlData)):
        sqlDataCache.append(sqlData[i][0])
    if email in sqlDataCache:
        cur.execute("SELECT pwd FROM account WHERE email='{}'".format(email))
        if pwd in cur.fetchone():
            cur.execute("SELECT block FROM account WHERE email='{}'".format(email))
            if cur.fetchone()[0] == 0:
                cur.close()
                con.close()
                return jsonify({'code':200})
            else:
                cur.close()
                con.close()
                return jsonify({'code':403})
        else:
            cur.close()
            con.close()
            return jsonify({'code':401})
    else:
        cur.close()
        con.close()
        return jsonify({'code':404})
@app.route('/feedback/',methods=['POST'])
def feedback():
    email = request.json.get('account')
    pwd = request.json.get('password')
    FBtype = request.json.get('feedback-type')
    FBinfo = request.json.get('feedback-info')
    con = sqlite3.connect('.mwl-githut-fb-data.db')
    cur = con.cursor()
    if FBtype in ['bug','warn','debug','want']:
        cur.execute('SELECT email FROM account')
        sqlData = cur.fetchall()
        sqlDataCache = []
        for i in range(len(sqlData)):
            sqlDataCache.append(sqlData[i][0])
        if email in sqlDataCache:
            cur.execute("SELECT pwd FROM account WHERE email='{}'".format(email))
            if pwd in cur.fetchone():
                cur.execute("SELECT block FROM account WHERE email='{}'".format(email))
                if cur.fetchone()[0] == 0:
                    cur.execute("SELECT user FROM account WHERE email='{}'".format(email))
                    if cur.fetchone()[0] == 0:
                        writeFeedback(account=email,accountLevel='user',level=FBtype,info=FBinfo)
                    else:
                        writeFeedback(account=email,accountLevel='organization',level=FBtype,info=FBinfo)
                    cur.close()
                    con.close()
                    return jsonify({'code':200})
                else:
                    cur.close()
                    con.close()
                    return jsonify({'code':403})
            else:
                cur.close()
                con.close()
                return jsonify({'code':401})
        else:
            cur.close()
            con.close()
            return jsonify({'code':404})
    else:
        cur.close()
        con.close()
        return jsonify({'code':400})
@app.route('/change',methods=['POST'])
def change():
    email = request.json.get('account')
    originPwd = request.json.get('origin')
    newPwd = request.json.get('new')
    con = sqlite3.connect('.mwl-githut-fb-data.db')
    cur = con.cursor()
    cur.execute('SELECT email FROM account')
    sqlData = cur.fetchall()
    sqlDataCache = []
    for i in range(len(sqlData)):
        sqlDataCache.append(sqlData[i][0])
    if email in sqlDataCache:
        cur.execute("SELECT pwd FROM account WHERE email='{}'".format(email))
        if originPwd in cur.fetchone():
            cur.execute("SELECT block FROM account WHERE email='{}'".format(email))
            if cur.fetchone()[0] == 0:
                cur.execute("UPDATE account SET pwd='{}' WHERE email='{}'".format(newPwd,email))
                con.commit()
                cur.close()
                con.close()
                return jsonify({'code':200})
            else:
                cur.close()
                con.close()
                return jsonify({'code':403})
        else:
            cur.close()
            con.close()
            return jsonify({'code':401})
    else:
        cur.close()
        con.close()
        return jsonify({'code':404})
@app.route('/register',methods=['POST'])
def register():
    if enableRegister:
        email = request.json.get('account')
        pwd = request.json.get('password')
        con = sqlite3.connect('.mwl-githut-fb-data.db')
        cur = con.cursor()
        cur.execute('SELECT email FROM account')
        sqlData = cur.fetchall()
        sqlDataCache = []
        for i in range(len(sqlData)):
            sqlDataCache.append(sqlData[i][0])
        if email not in sqlDataCache:
            if verifyEmail(email):
                cur.execute("INSERT INTO account VALUES ('{}','{}',0,0,0)".format(email,pwd))
                con.commit()
                cur.close()
                con.close()
                return jsonify({'code':200})
            else:
                cur.close()
                con.close()
                return jsonify({'code':400})
        else:
            cur.close()
            con.close()
            return jsonify({'code':409})
    else:
        return jsonify({'code':400})
@app.route('/register-organization',methods=['POST'])
def registerOrganization():
    if enableRegisterOrganization:
        email = request.json.get('account')
        pwd = request.json.get('password')
        con = sqlite3.connect('.mwl-githut-fb-data.db')
        cur = con.cursor()
        cur.execute('SELECT email FROM account')
        sqlData = cur.fetchall()
        sqlDataCache = []
        for i in range(len(sqlData)):
            sqlDataCache.append(sqlData[i][0])
        if email not in sqlDataCache:
            if verifyEmail(email):
                cur.execute("INSERT INTO account VALUES ('{}','{}',0,0,1)".format(email,pwd))
                con.commit()
                cur.close()
                con.close()
                return jsonify({'code':200})
            else:
                cur.close()
                con.close()
                return jsonify({'code':400})
        else:
            cur.close()
            con.close()
            return jsonify({'code':409})
    else:
        return jsonify({'code':400})


def writeFeedback(account,accountLevel,level,info):
    global file
    file.write('{} - {} - {} - {} - {}\n'.format(now.strftime('%Y-%m-%d %H:%M:%S'),account,accountLevel,level,info))
def clean():
    con = sqlite3.connect('.mwl-githut-fb-data.db')
    cur = con.cursor()
    cur.execute('select * from basicData')
    cache = cur.fetchone()
    cur.close()
    con.close()
    if cache[4] == 1:
        if cache[5] == 0:
            ipv4 = 'false'
        else:
            ipv4 = 'true'
        if cache[6] == 0:
            ipv6 = 'false'
        else:
            ipv6 = 'true'
        if osname == 'nt':
            jsonFile = open(r'feedback\feedback.json','w')
        else:
            jsonFile = open('feedback/feedback.json','w')
        jsonFile.write('"enabled":false,"ipv4":{},"ipv6":{},"link":"{}"'.format(ipv4,ipv6,cache[3]))
        jsonFile.close()
        if osname == 'nt':
            jsonFile = open(r'feedback\feedback-organization.json','w')
        else:
            jsonFile = open('feedback/feedback-organization.json','w')
        jsonFile.write('"enabled":false,"ipv4":{},"ipv6":{},"link":"{}"'.format(ipv4,ipv6,cache[3]))
        jsonFile.close()
    file.close()
registerExit(clean)
def run():
    print('API will launch in port 5000')
    app.run()