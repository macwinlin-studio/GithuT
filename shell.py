# coding=utf-8
# project: GitHub Tools Shell
# file: shell.py
# author: MacWinLin Studio CGK Team
# email: mwl@macwinlin.ml
# version: LTS(Long Term Support) 2.0.1
# Publish only on GitHub and MacWinLin Studio's GitLab.
# Copyright 2022 MacWinLin Studio.All rights reserved.
# Make unofficial GUI client please view core file.
print('Github Tools Shell 2.0.1')
from core.language_core import UpdateLanguage,cdatabase,rdatabase
from core.githut_core import run
from requests import get
from platform import platform
from json import loads
from os import mkdir,rename,remove
from shutil import rmtree
import sqlite3,logging
language = UpdateLanguage
language.reload(self=language)
class logClass:
    def __init__():
        logging.basicConfig(level=logging.DEBUG,filemode='a+',filename='githut-log.log',format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
    def debug(e):
        logging.debug(str(e))
    def info(e):
        logging.info(str(e))
    def warning(e):
        logging.warning(str(e))
    def error(e):
        logging.error(str(e))
    def critical(e):
        logging.critical(str(e))
    def exception(e):
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
    if state == 0:
        while True:
            tml = input('>')
            if tml != 'update':
                run(tml)
            else:
                updateFunction()
class Update():
    def latest(self):
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
        except Exception:
            log.warning('Could\'t get latest GitHub Tools version')
            return ['error']
        else:
            return [self.latestVersion,self.latestVersionLink,self.updateFile]
update = Update
def haveField(cur,field):
    try:
        cur.execute('select {} from data where id=1'.format(field))
    except sqlite3.OperationalError:
        log.warning('HaveFidle Check Program:Database didn\'t have \'{}\' field'.format(field))
        return False
    return True
# Update
def updateFunction():
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
