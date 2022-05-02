# coding=utf-8
import sqlite3
from json import dumps,loads
from datetime import date as time_date
from random import randint
from os.path import realpath,dirname,exists,isfile
from sys import path
from os import remove,mkdir,rename
from hashlib import sha256
from zipfile import ZipFile
from shutil import copy,rmtree
from platform import platform
path.append(dirname(realpath(__file__)))
from language_core import BackupLanguage
# project: GitHub Tools Backup Core
# file: backup_core.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: LTS(Long Term Support) 1.0
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
        cur = con.cursor()
        cur.execute("select * from data")
        cache = cur.fetchone()
        cache2 = {'ver':1.0,'data':[cache[1],cache[2],cache[3],cache[4],cache[5]]}
        # JSON
        self.backup = dumps(cache2)
        date = time_date.today()
        self.name = 'backup-' + str(date.year) + '-' + str(date.month) + '-' + str(date.day) + '-' + str(randint(100000,1000000))
    def save(self):
        language.reload()
        if not exists('BackupCache'):
            # Cache Directory
            mkdir('BackupCache')
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
            # ZIP File
            cache = self.name + '.zip'
            with ZipFile(cache, 'w') as z:
                for i in range(len(fileList)):
                    z.write(fileList[i])
            if 'Windows' in platform():
                cache = self.name + '.backup'
                if not exists(cache):
                    copy(realpath(self.name + '.zip'),dirname(realpath(__file__)))
                    rename(self.name + '.zip',cache)
                    remove('core\\' + self.name + '.zip')
                    print(language.filename + realpath(cache))
                    rmtree('BackupCache')
                else:
                    tml = input(language.replace)
                    if tml in ['y','Y','n','N']:
                        if tml in ['y','Y']:
                            if isfile(cache):
                                remove(cache)
                            else:
                                rmtree(cache)
                            copy(realpath(self.name + '.zip'),dirname(realpath(__file__)))
                            rename(self.name + '.zip',cache)
                            remove('core/' + self.name + '.zip')
                            print(language.filename + realpath(cache))
                            rmtree('BackupCache')
                        else:
                            print(language.backupC)
                    else:
                        print(language.replaceE)
            else:
                # Other Platform
                cache = self.name + '.backup'
                if not exists(cache):
                    copy(realpath(self.name + '.zip'),dirname(realpath(__file__)))
                    rename(self.name + '.zip',cache)
                    remove('core/' + self.name + '.zip')
                    print(language.filename + realpath(cache))
                    rmtree('BackupCache')
                else:
                    tml = input(language.replace)
                    if tml in ['y','Y','n','N']:
                        if tml in ['y','Y']:
                            if isfile(cache):
                                remove(cache)
                            else:
                                rmtree(cache)
                            copy(realpath(self.name + '.zip'),dirname(realpath(__file__)))
                            rename(self.name + '.zip',cache)
                            remove('core/' + self.name + '.zip')
                            print(language.filename + realpath(cache))
                            rmtree('BackupCache')
                        else:
                            print(language.backupC)
                    else:
                        print(language.replaceE)
        else:
            if isfile('BackupCache'):
                remove('BackupCache')
            else:
                rmtree('BackupCache')
            # Resave
            self.save()
# Import Backup File To Database
class Import():
    def __init__(self):
        language.reload()
        # Backup File Path
        self.path = input(language.path)
        # Open Backup File
        if self.path[-7:-1] + self.path[-1] == '.backup':
            if isfile(self.path):
                try:
                    with ZipFile(self.path,'r') as zip:
                        self.zipN = zip.namelist()
                except Exception as e:
                    print(language.pathE)
                    print(language.errorInfo + str(e))
                    self.zipN = ['backup-0000-0-00-000000.json','backup-0000-0-00-000000.sha256']
                    self.isBackup = 1
                else:
                    print(language.isBackup)
                    self.isBackup = 0
            else:
                print(language.pathE)
                self.isBackup = 1
        else:
            print(language.pathE)
            self.isBackup = 1
    def replace(self):
        # File number
        if not len(self.zipN) == 2:
            print(language.numberE)
        # File list verify change
        elif not (self.zipN[0][-5:-1] + 'n') == '.json' and (self.zipN[1][-7:-1] + '6') == '.sha256':
            if (self.zipN[0][-5:-1] + 'n') != '.json':
                self.zipN = [self.zipN[1],self.zipN[0]]
            if not (self.zipN[0][-5:-1] + 'n') == '.json' and (self.zipN[1][-7:-1] + '6') == '.sha256':
                print(language.structrueE)
            else:
                self.replace()
        else:
            # Remove and new
            if isfile('ImportBackupCache'):
                remove('ImportBackupCache')
            else:
                if exists('ImportBackupCache'):
                    rmtree('ImportBackupCache')
            mkdir('ImportBackupCache')
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
                print(language.errorInfo + str(e))
                file = open(backup_file_path + 'backup-0000-0-00-000000.json','w')
                file.close()
                file = open(backup_file_path + 'backup-0000-0-00-000000.sha256','w')
                file.close()
            else:
                print(language.canOpen)
            # Verify SHA256 value
            file = open(backup_file_path + self.zipN[0],'r',encoding='utf-8')
            self.json = file.read()
            file.close()
            file = open(backup_file_path + self.zipN[1],'r',encoding='utf-8')
            self.sha256 = file.read()
            file.close()
            if not sha256((self.json).encode('utf-8')).hexdigest() == self.sha256:
                print(language.sha256E)
            else:
                # JSON Load
                try:
                    self.jsonLoad = loads(self.json)
                except Exception as e:
                    print(language.jsonE)
                    print(language.errorInfo + str(e))
                else:
                    print(language.json)
                # Version and data
                try:
                    ver = self.jsonLoad['ver']
                    data = self.jsonLoad['data']
                except Exception as e:
                    print(language.readE)
                    print(language.errorInfo + str(e))
                    ver = 'error'
                    data = ['error']
                else:
                    print(language.read)
                # Import to database
                if ver == 1.0:
                    print(language.ver)
                    if len(data) == 5:
                        con = sqlite3.connect('.mwl-githut-data.db')
                        cur = con.cursor()
                        try:
                            cur.execute("DELETE FROM data WHERE id=1")
                            cache = "INSERT INTO data values (1,'{}',{},'{}',{},{})".format(*data)
                            cur.execute(cache)
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
                else:
                    print(language.verE)
        rmtree('ImportBackupCache')
