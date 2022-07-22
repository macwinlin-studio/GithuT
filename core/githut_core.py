# coding=utf-8
import sqlite3
from uuid import uuid3 as uuid
from uuid import NAMESPACE_DNS as uuid_NAMESPACE_DNS
from hashlib import sha256
from atexit import register
from ipaddress import ip_address as ipv
from platform import platform
from github import Github as github_Github
from os.path import dirname as os_path_dirname
from sys import path as sys_path
from sys import exit as sys_exit
from webbrowser import open_new as web_open
from requests import get as requests_get
from requests import post as requests_post
from os import remove as os_remove
from json import loads as json_loads
from os import name as oscore
sys_path.append(os_path_dirname(__file__))
import log_core as log
from language_core import languageC,globalLanguage,cdatabase,switchLanguage
from backup_core import Backup,Import
# project: GitHub Tools Core
# file: githut_core.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: 22w30b
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
def loadB() -> None:
    "Load basic information from database"
    global basic
    global ver
    global clearTokenInfo
    con = sqlite3.connect('.mwl-githut-data.db')
    log.info('Connected to database')
    cur = con.cursor()
    cur.execute('select * from data')
    cache = cur.fetchone()
    ver = cache[6]
    basic = [cache[2],cache[3],cache[4],cache[5],cache[13],cache[1]]
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
# Load Language
language = globalLanguage()
languageData = language.reload()
language = languageC()
language.reload(*languageData)
log.info('Load language module')
def confirmCore() -> list:
    "Confirm whether is GithuT core, and return uuid"
    return [True,str(uuid(uuid_NAMESPACE_DNS,basic[4]))]
# Space Data Function
def par(data2:str) -> list:
    "If I see space, I will cut it =|"
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
def get(start:int,text:str) -> str:
    "Hmm...Don't use it"
    return text[start:]
# About
def githut(data:str) -> None:
    "Get about info"
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
def config(data:str) -> None:
    "Config anythings, except can't config things"
    global clearTokenInfo
    if data == '':
        # Helper
        print(language.configH)
        log.info('Show config help')
    # Config 
    elif data[:5] == 'token':
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
    elif data[:8] == 'language':
        if data.strip() != 'language':
            if data[9:] in ['-u','--update']:
                log.info('Connect database')
                con = sqlite3.connect('.mwl-githut-data.db')
                cur = con.cursor()
                cur.execute('SELECT * FROM data')
                cache = cur.fetchone()[1]
                cur.close()
                con.close()
                log.info('Closed database')
                switchLanguage(cache,1)
            elif data[9:] != 'en-us':
                cache = switchLanguage(data[9:])
                if cache['code'] == 200:
                    print('[SUCCESS]' + cache['message'])
                else:
                    print('[ERROR]' + cache['message'])
            else:
                con = sqlite3.connect('.mwl-githut-data.db')
                cur = con.cursor()
                cur.execute("UPDATE data SET language='en-us' WHERE id=1")
                con.commit()
                cur.close()
                con.close()
                print('[SUCCESS]Updated language')
        else:
            if oscore == 'nt':
                cache = 'libs\\language-packages-cache\\info.json'
            else:
                cache = 'libs/language-packages-cache/info.json'
            print('Name: {}'.format(language.languagePackageInformation[0]))
            print('Date: {}'.format(language.languagePackageInformation[1]))
            print('Author: {}'.format(language.languagePackageInformation[2]))
            print('Broken: {}'.format(language.languagePackageInformation[3]))
            print('Website: {}'.format(language.languagePackageInformation[4]))
            print('Language: {}'.format(language.languagePackageInformation[5]))
    # Config Autologin
    elif data[:9] == 'autologin':
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
    elif data[:7] == 'develop':
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
    elif data[:2] == 'ct':
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
                    log.info('Enable auto clear token now')
                else:
                    print(language.NctY)
                    log.warning('Canceled change auto clear token enable state')
            else:
                if clearTokenInfo == 1:
                    cur.execute("UPDATE data SET clearToken=0 WHERE id=1")
                    con.commit()
                    log.info('Change database:cleartoken;OFF')
                    clearTokenInfo = 0
                    print(language.ctN)
                    log.info('Disable auto clear token now')
                else:
                    print(language.NctN)
                    log.warning('Canceled change auto clear token enable state')
        else:
            print(language.cerror)
            log.warning('Command not found')
        cur.close()
        con.close()
        log.info('Closed database')
    # Auto Check Update
    elif data[:6] == 'update':
        cache = get(7,data)
        con = sqlite3.connect('.mwl-githut-data.db')
        cur = con.cursor()
        cur.execute('select * from data')
        sql_cache = cur.fetchone()
        sql_cache = sql_cache[7]
        if cache in ['-y','--yes','-n','--no']:
            if cache == '-y' or cache == '--yes':
                if sql_cache == 0:
                    cur.execute('UPDATE data SET updateT=1 WHERE id=1')
                    con.commit()
                    log.info('Change database:auto-check-update;ON')
                    print(language.acuY)
                    log.info('Enable auto check update now')
                else:
                    print(language.NacuN)
                    log.warning('Canceled change auto check update enable state')
            else:
                if sql_cache == 1:
                    cur.execute('UPDATE data SET updateT=0 WHERE id=1')
                    con.commit()
                    log.info('Change database:auto-check-update;OFF')
                    print(language.acuN)
                    log.info('Disable auto check update now')
                else:
                    print(language.NacuN)
                    log.warning('Canceled change auto check update enable state')
        cur.close()
        con.close()
    # Update Server
    elif data[:3] == 'UPS' and data.strip() != 'UPS':
        cache = get(4,data)
        con = sqlite3.connect('.mwl-githut-data.db')
        cur = con.cursor()
        if cache[:7] == 'http://' or cache[:8] == 'https://':
            cur.execute("UPDATE data SET ups='{}' WHERE id=1".format(cache))
            con.commit()
        else:
            print(language.cerror)
        cur.close()
        con.close()
    elif data[:3] == 'LPS':
        cache = get(4,data)
        con = sqlite3.connect('.mwl-githut-data.db')
        log.info('Connected to database')
        cur = con.cursor()
        cur.execute("UPDATE data SET language_packages_link='{}' WHERE id=1".format(cache))
        con.commit()
        cur.close()
        con.close()
    # Command Error
    else:
        print(language.cerror)
        log.warning('Command not found')
# Set Account Type
def account(data:str) -> None:
    "Will report an error"
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
def loginF() -> None:
    "Login to GitHub"
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
def redata() -> None:
    "Rebuild database"
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
def crepo(data:str) -> None:
    "Create repository"
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
def drepo(data:str) -> None:
    "Delete repository"
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
def ctoken(data:str) -> None:
    pass
# Feedback
def feedback(jump:int=0) -> None:
    "Feedback to us or others team"
    global feedbackInfo
    def checkIP(ip:str) -> bool:
        ip_ver = ipv(ip)
        if ip_ver.version == 6:
            return True
        else:
            return False
    def domainNotHttp(domain:str) -> str:
        domainList = domain.split('/')
        if domainList[1] == '':
            return domainList[2]
        else:
            return domainList[1]
    con = sqlite3.connect('.mwl-githut-data.db')
    cur = con.cursor()
    cur.execute('select * from data')
    databaseCache = cur.fetchone()
    try:
        cache = requests_get(databaseCache[10] + '/feedback.json').text
        ip = requests_get('https://test.ipw.cn').text
    except Exception as e:
        print(language.couldtGetFeedbackServerInfo)
        log.warning('Could\'t get feedback server information')
        log.exception(e)
        return None
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
                    data = {'account':databaseCache[9],'password':sha256(password.encode()).hexdigest()}
                    try:
                        cache = requests_post(feedback_api + '/login',json=data).text
                    except Exception as e:
                        print(language.couldtLogin)
                        log.warning('Could\'t login')
                        log.exception(e)
                    else:
                        try:
                            cache = json_loads(cache)
                            temp = cache['code']
                            print('Feedback server:{}({})'.format(cache['org'],domainNotHttp(feedback_api)))
                        except Exception:
                            log.warning('Could\'t load JSON')
                            cache = {'code':400}
                        else:
                            log.info('Loaded JSON')
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
                        while True:
                            feedback_type = input(language.feedbackType)
                            if feedback_type in ['bug','warn','debug','want']:
                                break
                        lines = []
                        feedback_info = input(language.feedbackInfo)
                        while True:
                            lines.append(feedback_info)
                            feedback_info = input()
                            if feedback_info == ':w':
                                break
                        text = ''
                        for i in range(len(lines)):
                            text += lines[i]
                            text += '\n'
                        data = {'account':databaseCache[9],'password':sha256(feedbackInfo[1].encode()).hexdigest(),'feedback-type':feedback_type,'feedback-info':feedback_info}
                        try:
                            cache = requests_post(feedback_api + '/feedback',json=data).text
                        except Exception as e:
                            print(language.couldtFeedback + databaseCache[10] + '".')
                            log.warning('Could\'t feedback to "{}"'.format(databaseCache[10]))
                            log.exception(e)
                        else:
                            try:
                                cache = json_loads(cache)
                            except Exception:
                                log.warning('Could\'t load JSON')
                                cache = {'code':400}
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
def backupF() -> None:
    "Backup all database"
    backup = Backup()
    backup.save()
# Import Backup File
def importF() -> None:
    "Read backup file, then replace database, use file's texts"
    if oscore == 'nt':
        path = input(language.path_windows)
    else:
        path = input(language.path)
    cache = Import(path)
    if cache.isBackup == 0:
        cache.replace()
# Get Notice
def notice() -> None:
    "Get our notice"
    # Get notice
    try:
        cache = requests_get('https://githut.macwinlin.ml/notice.json').text
        cache = json_loads(cache)
        temp = [cache['org'],cache['version'],cache['data']]
    # Error
    except Exception as e:
        print(language.couldtNotice)
        log.warning('Could\'t get notice')
        log.exception(e)
    else:
        cache = cache['data']
        noticeLv0 = []
        noticeLv1 = []
        noticeLv2 = []
        noticeLv3 = []
        noticeLvN = []
        noticeLvU = []
        # Classification
        for i in range(len(cache)):
            if cache[i]['level'] == None:
                noticeLvN.append([cache[i]['time'],cache[i]['text']])
            elif cache[i]['level'] == 0:
                noticeLv0.append([cache[i]['time'],cache[i]['text']])
            elif cache[i]['level'] == 1:
                noticeLv1.append([cache[i]['time'],cache[i]['text']])
            elif cache[i]['level'] == 2:
                noticeLv2.append([cache[i]['time'],cache[i]['text']])
            elif cache[i]['level'] == 3:
                noticeLv3.append([cache[i]['time'],cache[i]['text']])
            else:
                noticeLvU.append([cache[i]['time'],cache[i]['text']])
        # Null Level
        print(language.noticeLvN)
        for i in range(len(noticeLvN)):
            print('{} | {}'.format(*noticeLvN[i]))
        # Level 0
        print(language.noticeLv0)
        for i in range(len(noticeLv0)):
            print('{} | {}'.format(*noticeLv0[i]))
        # Level 1
        print(language.noticeLv1)
        for i in range(len(noticeLv1)):
            print('{} | {}'.format(*noticeLv1[i]))
        # Level 2
        print(language.noticeLv2)
        for i in range(len(noticeLv2)):
            print('{} | {}'.format(*noticeLv2[i]))
        # Level 3
        print(language.noticeLv3)
        for i in range(len(noticeLv3)):
            print('{} | {}'.format(*noticeLv3[i]))
        # Unknown level
        print(language.noticeLvU)
        for i in range(len(noticeLvU)):
            print('{} | {}'.format(*noticeLvU[i]))
# Run Command
def run(data:str) -> None:
    "Not use any, only want a command :)"
    if data == 'help':
        print(language.help)
        log.info('Showed Help')
    elif data == 'where':
        tml = input('Develop text, read-only, confirm?(y/n)')
        if tml in ['y','Y']:
            print(__file__)
    elif data[:6] == 'config':
        if data == 'config':
            config('')
        else:
            config(get(7,data))
        log.info('Used config function')
    elif data[:6] == 'githut':
        if data == 'githut':
            githut('')
        else:
            githut(get(7,data))
        log.info('Used about function')
    elif data[:7] == 'account':
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
    elif data[:6] == 'create':
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
    elif data[:6] == 'delete':
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
    elif data == 'notice':
        notice()
    elif data in ['exit','quit']:
        sys_exit(0)
    else:
        print("'{}'".format(data) + language.notc)
        log.warning('Command not found')
# Exit
def clearToken() -> None:
    "Change database to clear it"
    if clearTokenInfo == 1:
        con = sqlite3.connect('.mwl-githut-data.db')
        cur = con.cursor()
        cur.execute("UPDATE data SET htoken=0 WHERE id=1")
        cur.execute("UPDATE data SET token='123456' WHERE id=1")
        con.commit()
        cur.close()
        con.close()
register(clearToken)
# Autologin
if basic[2] == 1:
    print(language.alogin)
    log.debug('Autologin start')
    loginF()