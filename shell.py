# coding=utf-8
# project: GitHub Tools Shell
# file: shell.py
# author: MacWinLin Studio CGK Team
# email: mwl@macwinlin.ml
# version: LTS(Long Term Support) 2.0.2
# Publish only on GitHub and MacWinLin Studio's GitLab.
# Copyright 2022 MacWinLin Studio.All rights reserved.
# Make unofficial GUI client please view core file.
print('Github Tools Shell 2.0.2')
from core.language_core import cdatabase,UpdateLanguage,globalLanguage,rdatabase,readLanguage
from core.githut_core import run
from requests import get
from platform import platform
from json import loads
from os import mkdir,rename,remove,name
from shutil import rmtree
import sqlite3,logging
language = globalLanguage()
languageData = language.reload('update')
language = UpdateLanguage()
language.reload(*languageData)
class logClass:
    "GithuT Shell's log class"
    def __init__():
        logging.basicConfig(level=logging.CRITICAL,filemode='a+',filename='githut-log.log',format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
    def debug(e):
        "Output debug info to log"
        logging.debug(str(e))
    def info(e):
        "Output normal info to log"
        logging.info(str(e))
    def warning(e):
        "Output warning info to log"
        logging.warning(str(e))
    def error(e): 
        "Output error info to log"
        logging.error(str(e))
    def critical(e):
        "Output critical info to log"
        logging.critical(str(e))
    def exception(e):
        "Output exception info to log"
        logging.exception(e)
log = logClass
# Connect to database and config basic information
con = sqlite3.connect('.mwl-githut-data.db')
log.info('Connected to database')
cur = con.cursor()
cur.execute('select * from data')
cache = cur.fetchone()
ver = cache[6]
auto = cache[7]
updateServer = cache[12]
cur.close()
con.close()
def main(state=0):
    "Main's main"
    if state == 0:
        while True:
            tml = input('>')
            if tml != 'update':
                run(tml)
            else:
                updateFunction()
class Update():
    "Update class"
    def latest(self):
        "Get GithuT's latest version"
        updateServerList = updateServer.split('/')
        if updateServerList[1] == '':
            updateServerNotHttp = updateServerList[2]
        else:
            updateServerNotHttp = updateServerList[1]
        try:
            cache = get(updateServer + '/latest.json')
            cache = cache.text
            cache = loads(cache)
            print('Queried {}({})'.format(cache['org'],updateServerNotHttp))
            self.latestVersion = cache['latest']
            self.latestVersionLink = cache['link']
            self.updateFile = cache['files']
            self.updateLanguage = cache['language']
        except Exception:
            log.warning('Could\'t get latest GitHub Tools version')
            return ['error']
        else:
            return [self.latestVersion,self.latestVersionLink,self.updateFile,self.updateLanguage]
update = Update
def haveField(cur: sqlite3.Cursor,field: str):
    "Check database whether or not have any field"
    try:
        cur.execute('select {} from data where id=1'.format(field))
    except sqlite3.OperationalError:
        log.warning('HaveField Check Program:Database didn\'t have \'{}\' field'.format(field))
        return False
    return True
# Update Language
def updateLanguage():
    "Update language package"
    # Verify link
    log.info('Connect database')
    con = sqlite3.connect('.mwl-githut-data.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM data")
    cache = cur.fetchone()
    languageServer = cache[14]
    language = cache[1]
    if languageServer[:8] == 'https://' or languageServer[:7] == 'http://':
        # Get JSON
        try:
            cache = get(languageServer + '/language-package-links.json').text
        except Exception:
            log.warning('language.switchLanguage: 400, Could\'t request language server')
            return {'code':400,'message':'Could\'t request language server'}
        else:
            log.info('language.switchLanguage: 200, Got JSON')
            # Load JSON
            try:
                cache = loads(cache)
            except Exception:
                log.warning('language.switchLanguage: 400, Cloud\'t load JSON')
                return {'code':400,'message':'Could\'t load JSON'}
            else:
                log.info('language.switchLanguage: 200, Loaded JSON')
                # Find Language Package
                try:
                    cache = cache[language]
                except Exception:
                    log.warning('language.switchLanguage: 400, Cloud\'t find language package')
                    return {'code':400,'message':'Could\'t find language package'}
                else:
                    # Get Language Pack
                    try:
                        cache = get(cache).text
                    except Exception:
                        log.warning('language.switchLanguage: 400, Could\'t get language package')
                        return {'code':400,'message':'Could\'t get language package'}
                    else:
                        if name == 'nt':
                            pathCache = 'core\\libs\\language-packages\\' + language + '.lpac'
                        else:
                            pathCache = 'core/libs/language-packages/' + language + '.lpac'
                        file = open(pathCache,'w')
                        file.write(cache)
                        file.close()
# Update
def updateFunction():
    "Main update function"
    log.info('Finding latest version')
    latest = update.latest(self=update)
    if len(latest) == 3:
        if ver != latest[0]:
            tml = input(language.haveNew)
            if tml in ['y','Y','n','N']:
                if tml in ['y','Y']:
                    fileCache = []
                    backupDatabaseId = rdatabase()
                    for i in range(len(latest[2])):
                        try:
                            print('Geting {} file'.format(latest[2][i]))
                            cache = get(latest[1] + latest[2][i]).text
                        except Exception as e:
                            print(language.downloadE)
                            log.error('Could\'t get update')
                            log.exception(e)
                        else:
                            print('Got {} file'.format(latest[2][i]))
                            fileCache.append(cache)
                    rename('core','core-backup')
                    log.info('Renamed original core dir to backup core dir')
                    mkdir('core')
                    log.info('Made new core dir')
                    if 'Windows' in platform():
                        for i in range(len(latest[2])):
                            cache = 'core\\' + latest[2][i]
                            file = open(cache,'w')
                            file.write(fileCache[i])
                            file.close()
                            log.info('Make new file \'{}\''.format(latest[2][i]))
                    else:
                        for i in range(len(latest[2])):
                            cache = 'core/' + latest[2][i]
                            file = open(cache,'w')
                            file.write(fileCache[i])
                            file.close()
                            log.info('Make new file \'{}\''.format(latest[2][i]))
                    log.info('Wrote file okay')
                    rmtree('core-backup')
                    log.info('Deleted backup dir')
                    con = sqlite3.connect('.mwl-githut-data.db')
                    cur = con.cursor()
                    cur.execute('select * from data')
                    cache = cur.fetchone()
                    backupDatabaseText = ['1',*list(cache[1:])]
                    cur.close()
                    con.close()
                    remove('.mwl-githut-data.db')
                    cdatabase()
                    con = sqlite3.connect('.mwl-githut-data.db')
                    cur = con.cursor()
                    for i in range(len(backupDatabaseId)):
                        if haveField(cur,backupDatabaseId[i]):
                            cache = 'UPDATE data SET {}={} WHERE id=1'.format(backupDatabaseId[i],backupDatabaseText[i])
                            cur.execute(cache)
                            con.commit()
                    cur.close()
                    con.close()
                    if latest[3] and readLanguage() != 'en-us':
                        print(language.updateLanguage)
                        mkdir('libs')
                        if name == 'nt':
                            cache = 'core\\libs\\'
                        else:
                            cache = 'core/libs/'
                        mkdir(cache)
                        mkdir(cache + 'language-packages')
                        cache = updateLanguage()
                        if cache['code'] == 200:
                            print('[SUCCESS]' + cache['message'])
                        else:
                            print('[ERROR]' + cache['message'])
                        print(language.browseDownload)
                    log.info('Updated to {}'.format(latest[0]))
                    print('Updated to {}'.format(latest[0]))
    else:
        log.info('This version is latest version now!')
        main()
if auto == 1:
    updateFunction()
    main()
else:
    main()
