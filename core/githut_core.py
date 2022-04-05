# coding=utf-8
import github,sqlite3
from os.path import realpath,dirname
from sys import path as sys_path
from webbrowser import open_new as web_open
from requests import get as requests_get
from os import remove as os_remove
sys_path.append(dirname(realpath(__file__)))
from language_core import languageC,cdatabase
# project: GitHub Tools Core
# file: githut_core.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: LTS(Long Term Support) 1.0
# Publish only on GitHub and MacWinLin Studio's GitLab.
# Copyright 2022 MacWinLin Studio.All rights reserved.
# This is core,if you try to make a unofficial GUI client,please not view gui/shell's codes.Maybe you will view many bugs.
# Make unofficial GUI client please contact mwl@macwinlin.ml.

# Code

# Load Basic Information,Autologin
basic = None
def loadB():
    global basic
    con = sqlite3.connect('.mwl-githut-data.db')
    cur = con.cursor()
    cur.execute('select * from data')
    cache = cur.fetchone()
    basic = [cache[2],cache[3],cache[4],cache[5]]
    cur.close()
    con.close()
loadB()

# Record Login State
loginV = 0
# Record Login Basic Information
g = None
user = None
l = None
# A Language Class
language = languageC()
# WARN!Try To Use Language Function,Please Use Reload Function First!Otherwise,Will Error!
# And If You Change Language,Please Restart Or Use Reload Function!
language.reload()
# Space Data Function
def par(data2):
    data = data2 + ' '
    turn = []
    cache = ''
    for i in range(len(data)):
        if data[i] == ' ':
            turn.append(cache)
            cache = ''
        else:
            cache += data[i]
    return turn
# Get Start To -1's Text
def get(start,text):
    return(text[start:-1] + text[-1])
# About
def githut(data):
    if data == '':
        print(language.githutH)
    elif data in ['-p','--program']:
        # About Program
        print(language.aboutPMT)
        print(language.aboutPMTgtv)
        print(language.aboutPMTpgv)
        print(language.aboutPMTpyv)
        print(language.aboutPMTgithub)
    elif data in ['-a','--author']:
        # About Author
        print(language.aboutAMT)
        print(language.aboutAMTauthor)
        print(language.aboutAMTmainD)
        print(language.aboutAMTverN)
        print(language.aboutAMTblog)
    elif data in ['-po','--program-open']:
        web_open('https://github.com/macwinlin-studio/GithuT/tree/1.0.0')
    elif data in ['-ao','--author-open']:
        web_open('https://blog.macwinlin.ml')
    elif data in ['-l','--license']:
        try:
            requests_get('https://test.xinxin2021.tk/itest')
        except:
            print(language.licenseE)
        else:
            print(requests_get('https://githut.macwinlin.ml/LICENSE').text)
    elif data in ['-c','--copyright']:
        print('Copyright © 2022 MacWinLin Studio.All rights reserved.')
    else:
        print(language.cerror)
# Config Language And Token
def config(data):
    if data == '':
        # Helper
        print(language.configH)
    # Config 
    elif data[0:5] == 'token':
        cache = get(6,data)
        cache2 = par(cache)
        con = sqlite3.connect('.mwl-githut-data.db')
        cur = con.cursor()
        cur.execute("select * from data")
        cache3 = cur.fetchone()
        if cache2[0] == 'add':
            if cache3[2] == 0:
                cur.execute("UPDATE data SET token=? WHERE id=?",(cache2[1],1))
                cur.execute("UPDATE data SET htoken=1 WHERE id=1")
                con.commit()
                basic[0] = 1
                basic[1] = cache2[1]
            else:
                print(language.hToken)
        elif cache2[0] == 'remove':
            if cache3[2] == 1:
                cur.execute("UPDATE data SET htoken=0 WHERE id=1")
                con.commit()
                basic[0] = 0
            else:
                print(language.nhToken)
        else:
            print(language.cerror)
        cur.close()
        con.close()
    # Config Language
    elif data[0:8] == 'language':
        cache = get(9,data)
        con = sqlite3.connect('.mwl-githut-data.db')
        cur = con.cursor()
        if cache in language.lList:
            cur.execute("UPDATE data SET language='" + cache + "' WHERE id=1")
            con.commit()
        else:
            print(language.cerror)
        language.reload()
        cur.close()
        con.close()
    # Config Autologin
    elif data[0:9] == 'autologin':
        cache = get(10,data)
        con = sqlite3.connect('.mwl-githut-data.db')
        cur = con.cursor()
        if cache in ['-y','--yes','-n','--no']:
            if cache == '-y' or cache == '--yes':
                if basic[3] == 0:
                    cur.execute("UPDATE data SET alogin=1 WHERE id=1")
                    con.commit()
                    basic[3] = 1
                    print(language.alY)
                else:
                    print(language.NalY)
            else:
                if basic[3] == 1:
                    cur.execute("UPDATE data SET alogin=0 WHERE id=1")
                    con.commit()
                    basic[3] = 0
                    print(language.alN)
                else:
                    print(language.NalN)
        else:
            print(language.cerror)
        cur.close()
        con.close()
    else:
        print(language.cerror)
# Set Account Type
def account(data):
    # Helper
    if data == '':
        print(language.accountH)
    elif data in ['-o','--organization','-u','--user']:
        con = sqlite3.connect('.mwl-githut-data.db')
        cur = con.cursor()
        if data in ['-o','--organization']:
            # Execute The Command
            if basic[2] == 0:
                basic[2] = 1
                cur.execute("UPDATE data SET account=1 WHERE id=1")
                con.commit()
            print(language.iso)
        else:
            # Execute The Command
            if basic[2] == 1:
                basic[2] = 0
                cur.execute("UPDATE data SET account=0 WHERE id=1")
                con.commit()
            print(language.isu)
    else:
        print(language.cerror)
# Login
def loginF():
    global g
    global user
    global l
    global login
    g = github.Github(login_or_token=basic[1])
    if basic[2] == 1:
        user = g.get_organization()
    else:
        user = g.get_user()
    if basic[0] == 0:
        print(language.nhToken)
    else:
        try:
            l = user.login
        except:
            print(language.terror)
        else:
            cache = language.loginS
            if basic[2] == 1:
                cache += language.loginSO
            else:
                cache += language.loginSU
            cache += l
            print(cache)
            login = 1
# Rebuild Database
def redata(data):
    os_remove('.mwl-githut-data.db')
    print(language.rdata)
    cdatabase()
    print(language.adata)
# Run Command
def run(data):
    if data == 'help':
        print(language.help)
    elif data[0:6] == 'config':
        if data == 'config':
            config('')
        else:
            config(get(7,data))
    elif data[0:6] == 'githut':
        if data == 'githut':
            githut('')
        else:
            githut(get(7,data))
    elif data[0:7] == 'account':
        if data == 'account':
            account('')
        else:
            account(get(8,data))
    elif data == 'login':
        loginF()
    elif data == 'redata':
        redata()
    else:
        print("'{}'".format(data) + language.notc)
if basic[3] == 1:
    print(language.alogin)
    loginF()