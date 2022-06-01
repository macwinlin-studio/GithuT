# coding=utf-8
import sqlite3,atexit
from ipaddress import ip_address as ipv
from platform import platform
from github import Github as github_Github
from os.path import realpath as os_path_realpath
from os.path import dirname as os_path_dirname
from sys import path as sys_path
from webbrowser import open_new as web_open
from requests import get as requests_get
from requests import post as requests_post
from os import remove as os_remove
from json import loads as json_loads
sys_path.append(os_path_dirname(os_path_realpath(__file__)))
import log_core as log
from language_core import languageC,cdatabase
from backup_core import Backup,Import
# project: GitHub Tools Core
# file: githut_core.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: LTS(Long Term Support) 1.0
# Publish only on GitHub and MacWinLin Studio's GitLab.
# Copyright 2022 MacWinLin Studio.All rights reserved.
# This is core,if you try to make a unofficial GUI client,please not view gui/shell's codes.Maybe you will view many bugs.
# Make unofficial GUI client please contact githut@macwinlin.ml.

# Code

# Start
log.info('Start GitHub Tools Alpha 0.2 Test Version')
log.info('Platform:' + platform())
# Load Basic Information,Autologin
basic = None
ver = None
feedbackInfo = [0,None]
clearTokenInfo = 0
def loadB():
    global basic
    global ver
    global clearTokenInfo
    con = sqlite3.connect('.mwl-githut-data.db')
    log.info('Connected to database')
    cur = con.cursor()
    cur.execute('select * from data')
    cache = cur.fetchone()
    ver = cache[6]
    basic = [cache[2],cache[3],cache[4],cache[5]]
    clearTokenInfo = cache[11]
    cur.close()
    con.close()
    log.info('Database closed')
loadB()
log.info('Version:' + ver)
log.info('Load basic information')
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
log.info('Load language module')
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
    return text[start:]
# About
def githut(data):
    if data == '':
        print(language.githutH)
        log.info('Showed help information')
    elif data in ['-p','--program']:
        # About Program
        print(language.aboutPMT)
        print(language.aboutPMTgtv)
        print(language.aboutPMTpgv)
        print(language.aboutPMTpyv)
        print(language.aboutPMTgithub)
        log.info('Showed about program')
    elif data in ['-a','--author']:
        # About Author
        print(language.aboutAMT)
        print(language.aboutAMTauthor)
        print(language.aboutAMTmainD)
        print(language.aboutAMTverN)
        print(language.aboutAMTblog)
        log.info('Show about author')
    elif data in ['-po','--program-open']:
        web_open('https://github.com/macwinlin-studio/GithuT/tree/a0.2')
        log.info('Open program website')
    elif data in ['-ao','--author-open']:
        web_open('https://blog.macwinlin.ml')
        log.info('Open author website')
    elif data in ['-l','--license']:
        try:
            requests_get('https://test.xinxin2021.tk/itest')
            log.debug('Try to get license file')
        except Exception:
            print(language.licenseE)
            log.warning('Could\'t get license file')
        else:
            print(requests_get('https://githut.macwinlin.ml/LICENSE').text)
            log.info('Show license file')
    elif data in ['-c','--copyright']:
        print('Copyright © 2022 MacWinLin Studio.All rights reserved.')
        log.info('Show copyright info')
    else:
        print(language.cerror)
        log.warning('Command not found')
# Config Language And Token
def config(data):
    if data == '':
        # Helper
        print(language.configH)
        log.info('Show config help')
    # Config 
    elif data[0:5] == 'token':
        cache = get(6,data)
        cache2 = par(cache)
        con = sqlite3.connect('.mwl-githut-data.db')
        log.info('Connected to database')
        cur = con.cursor()
        cur.execute("select * from data")
        cache3 = cur.fetchone()
        if cache2[0] == 'add':
            if data.strip() != 'token add':
                log.info('Have token data')
                if cache3[2] == 0:
                    cur.execute("UPDATE data SET token=? WHERE id=?",(cache2[1],1))
                    cur.execute("UPDATE data SET htoken=1 WHERE id=1")
                    con.commit()
                    log.info('Change database:token;add')
                    basic[0] = 1
                    basic[1] = cache2[1]
                    log.info('Add token')
                else:
                    print(language.hToken)
                    log.warning('Have a token')
            else:
                log.warning('Not have token data')
                print(language.peToken)
        elif cache2[0] == 'remove':
            if cache3[2] == 1:
                cur.execute("UPDATE data SET htoken=0 WHERE id=1")
                cur.execute("UPDATE data SET token='123456' WHERE id=1")
                con.commit()
                log.info('Change database:token;remove')
                basic[0] = 0
                log.info('Remove token')
            else:
                print(language.nhToken)
                log.warning('Not have token')
        else:
            print(language.cerror)
            log.warning('Command not found')
        cur.close()
        con.close()
        log.info('Database closed')
    # Config Language
    elif data[0:8] == 'language':
        if data.strip() != 'language':
            cache = get(9,data)
            con = sqlite3.connect('.mwl-githut-data.db')
            log.info('Connected to database')
            cur = con.cursor()
            # Search Language List
            if cache in language.lList:
                cur.execute("UPDATE data SET language='" + cache + "' WHERE id=1")
                con.commit()
                log.info('Change database:language;{}'.format(cache))
            else:
                print(language.cerror)
                log.warning('Could\'t change language')
            language.reload()
            cur.close()
            con.close()
            log.info('Database closed')
        else:
            print(language.cerror)
            log.warning('Command not found')
    # Config Autologin
    elif data[0:9] == 'autologin':
        cache = get(10,data)
        # Connect Database
        con = sqlite3.connect('.mwl-githut-data.db')
        log.info('Connected to database')
        cur = con.cursor()
        if cache in ['-y','--yes','-n','--no']:
            if cache == '-y' or cache == '--yes':
                if basic[2] == 0:
                    cur.execute("UPDATE data SET alogin=1 WHERE id=1")
                    con.commit()
                    log.info('Change database:autologin;ON')
                    basic[2] = 1
                    print(language.alY)
                    log.info('Enable autologin now')
                else:
                    print(language.NalY)
                    log.warning('Canceled change autologin enable state')
            else:
                if basic[2] == 1:
                    cur.execute("UPDATE data SET alogin=0 WHERE id=1")
                    con.commit()
                    log.info('Change database:autologin;OFF')
                    basic[2] = 0
                    print(language.alN)
                    log.info('Disable autologin now')
                else:
                    print(language.NalN)
                    log.warning('Canceled change autologin enable state')
        # Command Error
        else:
            print(language.cerror)
            log.warning('Command not found')
        cur.close()
        con.close()
        log.info('Database closed')
    # Develop Mode
    elif data[0:7] == 'develop':
        cache = get(7,data)
        # Connect Database
        con = sqlite3.connect('.mwl-githut-data.db')
        log.info('Connected to database')
        cur = con.cursor()
        if cache in ['-y','--yes','-n','--no']:
            if cache == '-y' or cache == '--yes':
                if basic[3] == 0:
                    cur.execute("UPDATE data SET developM=1 WHERE id=1")
                    con.commit()
                    log.info('Change database:develop-mode;ON')
                    basic[3] = 1
                    print(language.dmY)
                    log.info('Enable develop mode now')
                else:
                    print(language.NdmY)
                    log.warning('Canceled change develop mode enable state')
            else:
                if basic[3] == 1:
                    cur.execute("UPDATE data SET developM=0 WHERE id=1")
                    con.commit()
                    log.info('Change database:develop-mode;OFF')
                    basic[3] = 0
                    print(language.dmN)
                    log.info('Disable develop mode now')
                else:
                    print(language.NdmN)
                    log.warning('Canceled change develop mode enable state')
        else:
            print(language.cerror)
            log.warning('Command not found')
        cur.close()
        con.close()
        log.info('Database closed')
    # Auto clear token
    elif data[0:3] == 'ct':
        # Connect database
        con = sqlite3.connect('.mwl-githut-data.db')
        log.info('Connected to database')
        cur = con.cursor()
        cache = get(3,data)
        if cache in ['-y','--yes','-n','--no']:
            if cache == '-y' or cache == '--yes':
                if clearTokenInfo == 0:
                    cur.execute("UPDATE data SET clearToken=1 WHERE id=1")
                    con.commit()
                    log.info('Change database:clear token;ON')
                    clearTokenInfo = 1
                    print(language.ctY)
                else:
                    print(language.NctY)
            else:
                if clearTokenInfo == 1:
                    cur.execute("UPDATE data SET clearToken=0 WHERE id=1")
                    con.commit()
                    log.info('Change database:cleartoken;OFF')
                    clearTokenInfo = 0
                    print(language.ctN)
                else:
                    print(language.NctN)
        else:
            print(language.cerror)
            log.warning('Command not found')
    # Command Error
    else:
        print(language.cerror)
        log.warning('Command not found')
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
    # Global
    global g
    global user
    global l
    global loginV
    # GitHub
    g = github_Github(login_or_token=basic[1])
    # Get User
    user = g.get_user()
    # Have Token
    if basic[0] == 0:
        print(language.nhToken)
    else:
        # Login
        try:
            # Try To Login
            l = user.login
        except Exception as e:
            # Token Error
            print(language.terror)
            log.warning('Could\'t login to GitHub')
            log.exception(e)
        else:
            # OK
            cache = language.loginS
            # Username
            cache += language.loginSU
            cache += l
            # Name
            cache += language.Lname
            cache += user.name
            print(cache)
            loginV = 1
            log.info('Logined to GitHub')
# Rebuild Database
def redata():
    global basic
    global loginV
    os_remove('.mwl-githut-data.db')
    print(language.rdata)
    cdatabase()
    print(language.adata)
    basic = [0,None,0,0]
    loginV = 0
    log.info('Rebuild database')
# Create Repository
def crepo(data):
    if loginV == 1:
        # Create Repo
        try:
            user.create_repo(data)
        # Error
        except Exception as e:
            print(language.crepoE)
            log.warning('Could\'t create repository')
            log.exception(e)
        # Success
        else:
            print(language.crepoS)
            log.info('Created repository')
    else:
        print(language.ploginT)
        log.warning('Create repository:not login')
    # Develop mode
    if basic[3] == 1:
        drepo(data)
        log.info('Create repository:develop mode - delete repository')
# Delete Repository
def drepo(data):
    if loginV == 1:
        # Delete Repo
        try:
            repo = user.get_repo(data)
            repo.delete()
        # Error
        except Exception as e:
            print(language.drepoE)
            log.warning('Could\'t delete repository')
            log.exception(e)
        # Success
        else:
            print(language.drepoS)
            log.info('Deleted repository')
    else:
        print(language.ploginT)
        log.warning('Delete repository:not login')
    # Develop mode
    if basic[3] == 1:
        crepo(data)
        log.info('Delete repository:develop mode - create repository')
# Create Token
def ctoken(data):
    pass
# Feedback
def feedback(jump=0):
    global feedbackInfo
    def checkIP(ip):
        ip_ver = ipv(ip)
        if ip_ver.version == 6:
            return True
        else:
            return False
    con = sqlite3.connect('.mwl-githut-data.db')
    cur = con.cursor()
    cur.execute('select * from data')
    databaseCache = cur.fetchone()
    try:
        cache = requests_get(databaseCache[10]).text
        ip = requests_get('https://test.ipw.cn').text
    except Exception as e:
        print(language.couldtGetFeedbackServerInfo)
        log.warning('Could\'t get feedback server information')
        log.exception(e)
    else:
        log.info('Got feedback server information')
    cache = json_loads(cache)
    feedback_api = cache['link']
    if cache['enabled']:
        if (not cache['ipv4'] and cache['ipv6']) or jump == 1:
            if checkIP(ip):
                if databaseCache[8] == 1:
                    if feedbackInfo[0] == 0:
                        password = input(language.feedbackGetPassword)
                        feedbackInfo = [1,password]
                    else:
                        password = feedbackInfo[1]
                    data = {'account':databaseCache[9],'password':password}
                    try:
                        cache = requests_post(feedback_api + '/login',data).text
                    except Exception as e:
                        print(language.couldtLogin)
                        log.warning('Could\'t login')
                        log.exception(e)
                    else:
                        cache = json_loads(cache)
                        if cache['code'] == 200:
                            print(language.loginSuccess)
                            log.info('Login to feedback server:"{}"'.format(databaseCache[10]))
                        elif cache['code'] == 401:
                            print(language.passwordError)
                            log.warning('Login to feedback server:"{}" error[:]password error'.format(databaseCache[10]))
                        elif cache['code'] == 404:
                            print(language.userNotFound)
                            log.warning('Login to feedback server:"{}" error[:]user is not exist'.format(databaseCache[10]))
                        elif cache['code'] == 500:
                            print(language.serverError)
                            log.warning('Login to feedback server:"{}" error[:]feedback server error'.format(databaseCache[10]))
                        else:
                            print(language.unknownError)
                            log.warning('Login to feedback server:"{}" error[:]unknown error'.format(databaseCache[10]))
                        while feedback_type in ['bug','warn','debug']:
                            feedback_type = input(language.feedbackType)
                        lines = []
                        feedback_info = input(language.feedbackInfo)
                        while feedback_info != ':w':
                            lines.append(feedback_info)
                            feedback_info = input()
                        text = ''
                        for i in range(len(lines)):
                            text += lines[i]
                            text += '\n'
                        data = {'account':databaseCache[9],'password':feedbackInfo[1],'feedback-type':feedback_type,'feedback-info':feedback_info}
                        try:
                            cache = requests_post('https://feedback-githut.macwinlin.ml/feedback').text
                        except Exception as e:
                            print(language.couldtFeedback + databaseCache[10] + '".')
                            log.warning('Could\'t feedback to "{}"'.format(databaseCache[10]))
                            log.exception(e)
                        else:
                            cache = json_loads(cache)
                            if cache['code'] == 200:
                                print(language.feedbackSuccess)
                                log.warning('Feedback to feedback server:"{}"'.format(databaseCache[10]))
                            elif cache['code'] == 401:
                                print(language.passwordError)
                                log.warning('Feedback to feedback server:"{}" error[:]password error'.format(databaseCache[10]))
                            elif cache['code'] == 403:
                                print(language.blocked)
                                log.warning('Feedback to feedback server:"{}" error[:]blocked'.format(databaseCache[10]))
                            elif cache['code'] == 404:
                                print(language.userNotFound)
                                log.warning('Feedback to feedback server:"{}" error[:]user is not exist'.format(databaseCache[10]))
                            elif cache['code'] == 500:
                                print(language.serverError)
                                log.warning('Feedback to feedback server:"{}" error[:]feedback server error'.format(databaseCache[10]))
                            else:
                                print(language.unknownError)
                                log.warning('Feedback to feedback server:"{}" error[:]unknown error'.format(databaseCache[10]))
                        cur.close()
                        con.close()
                else:
                    admin = input(language.feedbackGetAdmin)
                    cur.execute('UPDATE data SET feedback_admin=? WHERE id=?',(admin,1))
                    con.commit()
                    cur.close()
                    con.close()
                    feedback()
            else:
                print(language.notSupportIPv6)
        else:
            feedback(jump=1)
    else:
        print(language.feedbackServerClose)
        log.warning('Feedback server is closed')
# Backup
def backupF():
    backup = Backup()
    backup.save()
# Import Backup File
def importF():
    cache = Import()
    if cache.isBackup == 0:
        cache.replace()
# Run Command
def run(data):
    if data == 'help':
        print(language.help)
        log.info('Showed Help')
    elif data[0:6] == 'config':
        if data == 'config':
            config('')
        else:
            config(get(7,data))
        log.info('Used config function')
    elif data[0:6] == 'githut':
        if data == 'githut':
            githut('')
        else:
            githut(get(7,data))
        log.info('Used about function')
    elif data[0:7] == 'account':
        print('Deactivated command.')
        #if data == 'account':
            #account('')
        #else:
            #account(get(8,data))
        log.warning('Set account type:deactivated command')
    elif data == 'login':
        loginF()
        log.info('Used login function')
    elif data == 'redata':
        redata()
        log.info('Used rebuild function')
    elif data[0:6] == 'create':
        if data == 'create':
            print(language.createH)
            log.info('Show create help')
        elif data[7:11] == 'repo':
            if get(7,data) == 'repo':
                run('create')
            else:
                crepo(get(12,data))
                log.info('Use create repository function')
        else:
            print("'{}'".format(data) + language.notc)
            log.warning('Command not found')
    elif data == 'backup':
        backupF()
        log.info('Used backup function')
    elif data == 'import':
        importF()
        log.info('Used import backup function')
    elif data == 'feedback':
        feedback()
        log.info('Used feedback function')
    elif data[0:6] == 'delete':
        if data == 'delete':
            print(language.deleteH)
            log.info('Show delete help')
        elif data[7:11] == 'repo':
            if get(7,data) == 'repo':
                run('delete')
            else:
                drepo(get(12,data))
                log.info('Used delete repository function')
        else:
            print("'{}'".format(data) + language.notc)
            log.warning('Command not found')
    else:
        print("'{}'".format(data) + language.notc)
        log.warning('Command not found')
# Exit
@atexit.register
def clearToken():
    if clearTokenInfo == 1:
        con = sqlite3.connect('.mwl-githut-data.db')
        cur = con.cursor()
        cur.execute("UPDATE data SET htoken=0 WHERE id=1")
        cur.execute("UPDATE data SET token='123456' WHERE id=1")
        con.commit()
        cur.close()
        con.close()
# Autologin
if basic[2] == 1:
    print(language.alogin)
    log.debug('Autologin start')
    loginF()