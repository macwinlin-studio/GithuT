# coding=utf-8
import sqlite3,api
from os import name,system
from sys import exit as sysExit
from hashlib import sha256
from getpass import getpass
# project: GitHub Tools Feedback Serve
# file: main.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: LTS(Long Term Support) 1.0
# Publish only on GitHub and MacWinLin Studio's GitLab.
# Copyright 2022 MacWinLin Studio.All rights reserved.

# Code

def main(user,cur='#',level=2):
    while True:
        tml = input('{}{} '.format(user,cur))
        # Help
        if tml == 'help':
            print('''CPwd                            Change Password
enable register                 Enable Register
enable register-organization    Enable Register Organization
disable register                Disable Register
disable register-organization   Disable Register Organization
run                             Launch API Module
exit                            Exit Program''')
        # Change password
        elif tml == 'CPwd':
            con = sqlite3.connect('.mwl-githut-fb-data.db')
            SQLcur = con.cursor()
            SQLcur.execute('SELECT * FROM account')
            sqlData = SQLcur.fetchone()
            originPwd = getpass('Please enter origin password:')
            if sha256(originPwd.encode()).hexdigest() == sqlData[1]:
                newPwd = getpass('Please enter new password:')
                newPwdA = getpass('Please enter new password again:')
                if newPwd == newPwdA:
                    SQLcur.execute("UPDATE account SET pwd=? WHERE email=?",(sha256(newPwd.encode()).hexdigest(),user))
                    con.commit()
                    print('Changed password')
        elif tml == 'enable register':
            con = sqlite3.connect('.mwl-githut-fb-data.db')
            SQLcur = con.cursor()
            if level >= 1:
                SQLcur.execute('UPDATE basicData SET register=1 WHERE id=1')
                con.commit()
            else:
                print('Your level is low,could\'t operate')
        elif tml == 'disable register':
            con = sqlite3.connect('.mwl-githut-fb-data.db')
            SQLcur = con.cursor()
            if level >= 1:
                SQLcur.execute('UPDATE basicData SET register=0 WHERE id=1')
                con.commit()
            else:
                print('Your level is low,could\'t operate')
        elif tml == 'enable register-organization':
            con = sqlite3.connect('.mwl-githut-fb-data.db')
            SQLcur = con.cursor()
            if level >= 2:
                SQLcur.execute('UPDATE basicData SET registerOrganization=1 WHERE id=1')
                con.commit()
            else:
                print('Your level is low,could\'t operate')
        elif tml == 'disable register-organization':
            con = sqlite3.connect('.mwl-githut-fb-data.db')
            SQLcur = con.cursor()
            if level >= 2:
                SQLcur.execute('UPDATE basicData SET registerOrganization=0 WHERE id=1')
                con.commit()
            else:
                print('Your level is low,could\'t operate')
        elif tml[:3] == 'ban':
            if level >= 1:
                con = sqlite3.connect('.mwl-githut-fb-data.db')
                SQLcur = con.cursor()
                name = tml[4:]
                SQLcur.execute('SELECT email FROM account')
                sqlData = SQLcur.fetchall()
                sqlDataCache = []
                for i in range(len(sqlData)):
                    sqlDataCache.append(sqlData[i][0])
                if name in sqlDataCache:
                    SQLcur.execute("UPDATE account SET block=1 WHERE email='{}'".format(name))
                    con.commit()
                    print('Baned {}'.format(name))
                else:
                    print('Didn\'t have {} account'.format(name))
            else:
                print('Your level is low,could\'t operate')
        elif tml[:5] == 'deban':
            if level >= 1:
                con = sqlite3.connect('.mwl-githut-fb-data.db')
                SQLcur = con.cursor()
                name = tml[6:]
                SQLcur.execute('SELECT email FROM account')
                sqlData = SQLcur.fetchall()
                sqlDataCache = []
                for i in range(len(sqlData)):
                    sqlDataCache.append(sqlData[i][0])
                if name in sqlDataCache:
                    SQLcur.execute("UPDATE account SET block=0 WHERE email='{}'".format(name))
                    con.commit()
                    print('Debaned {}'.format(name))
                else:
                    print('Didn\'t have {} account'.format(name))
            else:
                print('Your level is low,could\'t operate')
        elif tml == 'run':
            print('Please send your feedback file to githut@macwinlin.ml every month(enter your feedback organization username)')
            con = sqlite3.connect('.mwl-githut-fb-data.db')
            SQLcur = con.cursor()
            SQLcur.execute('SELECT * FROM basicData')
            cache = SQLcur.fetchone()
            api.start(cache[1],cache[2])
            api.run()
        elif tml == 'exit':
            sysExit(0)
        else:
            print('Command error')
def clearScreen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')
if __name__ == '__main__':
    print('GitHub Tools Feedback Serve 1.0')
    print('This project don\'t generate register website,only generate API')
    con = sqlite3.connect('.mwl-githut-fb-data.db')
    cur = con.cursor()
    cur.execute("select * from account where email='root'")
    sqlData = cur.fetchone()
    password = input('Please enter ROOT password:')
    clearScreen()
    print('GitHub Tools Feedback Serve 1.0')
    print('This project don\'t generate register website,only generate API')
    print('Please enter ROOT password:{}'.format(len(password) * '*'))
    if sha256((password.strip()).encode()).hexdigest() == sqlData[1]:
        cur.close()
        con.close()
        if sqlData[0] == 0:
            main(user=sqlData[0],cur='$',level=0)
        elif sqlData[0] == 1:
            main(user=sqlData[0],cur='@',level=1)
        else:
            main(user=sqlData[0])
    else:
        print('Password error!')
        cur.close()
        con.close()
        sysExit()