# coding=utf-8
import sqlite3
from json import dumps,loads
from datetime import date as time_date
from random import randint
from os.path import realpath,dirname,exists,isfile,abspath
from sys import path
from os import remove,mkdir,rename
from hashlib import sha256
from zipfile import ZipFile
from shutil import rmtree
from platform import platform
path.append(dirname(realpath(__file__)))
from language_core import BackupLanguage
import log_core as log
# project: GitHub Tools Backup Core
# file: backup_core.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: 22w25a
# Publish only on GitHub and MacWinLin Studio's GitLab.
# Copyright 2022 MacWinLin Studio.All rights reserved.

# Code

# Load Language
language = BackupLanguage()
# Backup Database
class Backup():
    def __init__(self):
        # Read data
        con = sqlite3.connect('.mwl-githut-data.db')
        log.info('Connect to database')
        cur = con.cursor()
        cur.execute("select * from data")
        cache = cur.fetchone()
        cache2 = {'ver':1.2,'data':[*cache[1:6],'a0.2-22w25a',cache[7:]]}
        # JSON
        self.backup = dumps(cache2)
        date = time_date.today()
        self.name = 'backup-' + str(date.year) + '-' + str(date.month) + '-' + str(date.day) + '-' + str(randint(100000,1000000))
        cur.close()
        con.close()
        log.info('Database closed')
    def save(self):
        log.info('Saving backup file')
        language.reload()
        log.info('Load language module')
        if not exists('BackupCache'):
            # Cache Directory
            mkdir('BackupCache')
            log.info('Make cache dir')
            fileList = []
            # Cache
            if 'Windows' in platform():
                cache = 'BackupCache\\' + self.name + '.json'
                fileList.append(cache)
                file = open(cache,'w')
                file.write(self.backup)
                file.close()
                cache = 'BackupCache\\' + self.name + '.sha256'
                fileList.append(cache)
                file = open(cache,'w')
                file.write(sha256(self.backup.encode('utf-8')).hexdigest())
                file.close()
                log.info('Make cache files')
            # Other Platform
            else:
                cache = 'BackupCache/' + self.name + '.json'
                fileList.append(cache)
                file = open(cache,'w')
                file.write(self.backup)
                file.close()
                cache = 'BackupCache/' + self.name + '.sha256'
                fileList.append(cache)
                file = open(cache,'w')
                file.write(sha256(self.backup.encode('utf-8')).hexdigest())
                file.close()
                log.info('Make cache files')
            # ZIP File
            cache = self.name + '.zip'
            with ZipFile(cache, 'w') as z:
                for i in range(len(fileList)):
                    z.write(fileList[i])
            log.info('Make ZIP File')
            if 'Windows' in platform():
                cache = self.name + '.backup'
                if not exists(cache):
                    rename(self.name + '.zip',cache)
                    log.info('Renamed ZIP File')
                    print(language.filename + abspath(cache))
                    rmtree('BackupCache')
                else:
                    tml = input(language.replace)
                    if tml in ['y','Y','n','N']:
                        if tml in ['y','Y']:
                            if isfile(cache):
                                remove(cache)
                            else:
                                rmtree(cache)
                            rename(self.name + '.zip',cache)
                            log.info('Overwrited backup file')
                            log.info('Renamed ZIP File')
                            print(language.filename + abspath(cache))
                            rmtree('BackupCache')
                        else:
                            print(language.backupC)
                            log.warning('Canceled overwrite backup file')
                    else:
                        print(language.replaceE)
                        log.warning('')
            else:
                # Other Platform
                cache = self.name + '.backup'
                if not exists(cache):
                    rename(self.name + '.zip',cache)
                    log.info('Renamed ZIP File')
                    print(language.filename + abspath(cache))
                    rmtree('BackupCache')
                else:
                    tml = input(language.replace)
                    if tml in ['y','Y','n','N']:
                        if tml in ['y','Y']:
                            if isfile(cache):
                                remove(cache)
                            else:
                                rmtree(cache)
                            rename(self.name + '.zip',cache)
                            log.info('Overwrited backup file')
                            log.info('Renamed ZIP File')
                            print(language.filename + abspath(cache))
                            rmtree('BackupCache')
                        else:
                            print(language.backupC)
                    else:
                        print(language.replaceE)
                        log.warning('Canceled overwrite backup file')
        else:
            log.warning('Have dir "BackupCache"')
            if isfile('BackupCache'):
                remove('BackupCache')
            else:
                rmtree('BackupCache')
            log.info('Removed dir "BackupCache"')
            # Resave
            self.save()
# Import Backup File To Database
class Import():
    def __init__(self):
        language.reload()
        log.info('Load language module')
        # Backup File Path
        self.path = input(language.path)
        log.info('Got backup file path')
        # Open Backup File
        if self.path[-7:] == '.backup':
            log.info('Path suffix is .backup')
            if isfile(self.path):
                log.info('Is a file')
                try:
                    with ZipFile(self.path,'r') as zip:
                        self.zipN = zip.namelist()
                except Exception as e:
                    print(language.pathE)
                    log.warning('Could\'t open backup(ZIP) file')
                    log.exception(e)
                    self.zipN = ['backup-0000-0-00-000000.json','backup-0000-0-00-000000.sha256']
                    self.isBackup = 1
                    log.error('Not is backup file')
                else:
                    print(language.isBackup)
                    self.isBackup = 0
                    log.info('Is backup file')
            else:
                print(language.pathE)
                self.isBackup = 1
                log.error('Not is a file')
        else:
            print(language.pathE)
            self.isBackup = 1
            log.error('Backup file suffix is .backup')
    def replace(self):
        # File number
        if not len(self.zipN) == 2:
            print(language.numberE)
            log.error('Backup file\'s file number error')
        # File list verify change
        elif not (self.zipN[0][-5:]) == '.json' and (self.zipN[1][-7:]) == '.sha256':
            if (self.zipN[0][-5:]) != '.json':
                self.zipN = [self.zipN[1],self.zipN[0]]
                log.error('File suffix error in backup file')
            if not (self.zipN[0][-5:]) == '.json' and (self.zipN[1][-7:]) == '.sha256':
                print(language.structrueE)
                log.error('Could\'t fix this error')
            else:
                self.replace()
                log.info('Fixed,restart')
        else:
            # Remove and new
            if isfile('ImportBackupCache'):
                log.warning('Have file "ImportBackupCache"')
                remove('ImportBackupCache')
                log.info('Remove file "ImportBackupCache"')
            else:
                if exists('ImportBackupCache'):
                    log.warning('Have dir "ImportBackupCache"')
                    rmtree('ImportBackupCache')
                    log.info('Remove dir "ImportBackupCache"')
            mkdir('ImportBackupCache')
            log.info('Make cache dir')
            # Windows/Linux
            if 'Windows' in platform():
                backup_file_path = 'ImportBackupCache\\'
            else:
                backup_file_path = 'ImportBackupCache/'
            # Open Zip File
            try:
                with ZipFile(self.path,'r') as zip:
                    zip.extractall('ImportBackupCache')
            except Exception as e:
                print(language.cantOpen)
                file = open(backup_file_path + 'backup-0000-0-00-000000.json','w')
                file.close()
                file = open(backup_file_path + 'backup-0000-0-00-000000.sha256','w')
                file.close()
                log.warning('Could\'t extract backup file')
                log.exception(e)
            else:
                print(language.canOpen)
                log.info('Extract backup file')
            # Verify SHA256 value
            file = open(backup_file_path + self.zipN[0],'r',encoding='utf-8')
            self.json = file.read()
            file.close()
            file = open(backup_file_path + self.zipN[1],'r',encoding='utf-8')
            self.sha256 = file.read()
            file.close()
            if not sha256((self.json).encode('utf-8')).hexdigest() == self.sha256:
                print(language.sha256E)
                log.error('Could\'t verify backup file')
            else:
                # JSON Load
                try:
                    self.jsonLoad = loads(self.json)
                except Exception:
                    print(language.jsonE)
                    log.warning('Could\'t load json data')
                else:
                    print(language.json)
                    log.info('Loaded json data')
                # Version and data
                try:
                    ver = self.jsonLoad['ver']
                    data = self.jsonLoad['data']
                except Exception as e:
                    print(language.readE)
                    log.warning('Could\'t read backup module version and backup data')
                    log.exception(e)
                    ver = 'error'
                    data = ['error']
                else:
                    print(language.read)
                # Import to database
                if ver == 1.2:
                    log.info('Support this backup module version')
                    print(language.ver)
                    if len(data) == 11:
                        con = sqlite3.connect('.mwl-githut-data.db')
                        cur = con.cursor()
                        try:
                            cur.execute("DELETE FROM data WHERE id=1")
                            cache = "INSERT INTO data values (1,'{}',{},'{}',{},{},'a0.2-22w25a',{},{},'{}','{}',{})".format(*data)
                            cur.execute(cache)
                            con.commit()
                        except Exception as e:
                            con.rollback()
                            print(language.importE)
                            log.warning('Could\'t import backup data to database')
                            log.exception(e)
                        else:
                            print(language.importS)
                            log.info('Imported backup data to database')
                        cur.close()
                        con.close()
                    else:
                        print(language.lenE)
                elif ver == 1.1:
                    log.info('Support this backup module version')
                    con = sqlite3.connect('.mwl-githut-data.db')
                    cur = con.cursor()
                    cur.execute('select * from data')
                    cache = cur.fetchone()
                    print(language.ver)
                    if len(data) == 7:
                        try:
                            cur.execute("DELETE FROM data WHERE id=1")
                            sql_cache = "INSERT INTO data values (1,'{}',{},'{}',{},{},'a0.2-22w25a',{},{},'{}','{}')".format(*data,cache[8:])
                            cur.execute(sql_cache)
                            con.commit()
                        except Exception as e:
                            con.rollback()
                            print(language.importE)
                            log.warning('Could\'t import backup data to database')
                            log.exception(e)
                        else:
                            print(language.importS)
                            log.info('Imported backup data to database')
                        cur.close()
                        con.close()
                    else:
                        print(language.lenE)
                elif ver == 1.0:
                    log.info('Support this backup module version')
                    con = sqlite3.connect('.mwl-githut-data.db')
                    cur = con.cursor()
                    cur.execute('select * from data')
                    cache = cur.fetchone()
                    print(language.ver)
                    if len(data) == 5:
                        try:
                            cur.execute("DELETE FROM data WHERE id=1")
                            cache = ''
                            sql_cache = "INSERT INTO data values (1,'{}',{},'{}',{},{},'a0.2-22w25a',{})".format(*data,cache[7:])
                            cur.execute(sql_cache)
                            con.commit()
                        except Exception as e:
                            con.rollback()
                            print(language.importE)
                            print(language.errorInfo + str(e))
                        else:
                            print(language.importS)
                        cur.close()
                        con.close()
                    else:
                        print(language.lenE)
                    cur.close()
                    con.close()
                else:
                    print(language.verE)
                    log.warning('Don\'t support this backup module version')
        rmtree('ImportBackupCache')
        log.info('Remove cache dir')
