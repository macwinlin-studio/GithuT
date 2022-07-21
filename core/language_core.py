# coding=utf-8
import sqlite3
from os.path import isfile as os_path_isfile
from os.path import isdir as os_path_isdir
from os.path import exists as os_path_exists
from os import rmdir as os_rmdir
from platform import platform
from os import popen as os_popen
from requests import get as requests_get
from json import loads as json_loads
from os import name as oscore
from os import remove as os_remove
from os import mkdir as os_mkdir
from sys import path as sys_path
from os.path import dirname as os_path_dirname
sys_path.append(os_path_dirname(__file__))
import log_core as log
# project: GitHub Tools Language Core
# file: language_core.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: 22w30a
# Publish only on GitHub and MacWinLin Studio's GitLab.
# Copyright 2022 MacWinLin Studio.All rights reserved.

# Code

# Define Read Language
def readLanguage() -> str:
        "Get language from database, then return"
        con = sqlite3.connect('.mwl-githut-data.db')
        cur = con.cursor()
        cur.execute('select * from data')
        cache = cur.fetchone()
        cur.close()
        con.close()
        return cache[1]
# Define Create Databese
def cdatabase() -> None:
    "Create a new database"
    con = sqlite3.connect('.mwl-githut-data.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY,language TEXT NOT NULL DEFAULT 'en-us',htoken INTEGER NOT NULL DEFAULT 0,token TEXT,alogin INTEGER NOT NULL DEFAULT 0,developM INTEGER NOT NULL DEFAULT 0,version TEXT NOT NULL DEFAULT 'a0.2-22w30a',updateT INTEGER NOT NULL DEFAULT 1,feedback INTEGER NOT NULL DEFAULT 0,feedback_admin TEXT,feedback_link TEXT NOT NULL DEFAULT 'https://githut.macwinlin.ml/feedback.json',clearToken INTEGER NOT NULL DEFAULT 0,ups TEXT NOT NULL DEFAULT 'https://githut.macwinlin.ml/update',will_delete_at_next_change_database INTEGER NOT NULL DEFAULT 0,language_packages_link TEXT NOT NULL DEFAULT 'https://githut.macwinlin.ml/language-packages')")
    cur.execute("INSERT INTO data values (1,'en-us',0,'123456',0,0,'a0.2-22w30a',1,0,'123456','https://githut.macwinlin.ml',0,'https://githut.macwinlin.ml/update',0,'https://githut.macwinlin.ml/language-packages')")
    con.commit()
    cur.close()
    con.close()
    if 'Windows' in platform():
        os_popen('attrib +H .mwl-githut-data.db')
# Define Read Database
def rdatabase() -> list:
    "Return all database, but no datas"
    return ['id','language','htoken','token','alogin','developM','version','updateT','feedback','feedback_admin','feedback_link','clearToken','ups','will_delete_at_next_change_database','language_packages_link']
# Create Database
if not os_path_isfile('.mwl-githut-data.db'):
    if os_path_isdir('.mwl-githut-data.db'):
        os_rmdir('.mwl-githut-data.db')
    cdatabase()
# Many lines text
def linesText(texts: list) -> str:
    "A list -> Multiline text"
    cache = texts[0] + '\n'
    for i in range(len(texts) - 1):
        cache += texts[i + 1]
        if (i + 2) != len(texts):
            cache += '\n'
# Switch Language
def switchLanguage(language: str,update=0) -> dict:
    "Switch language, download from packages server"
    # Verify link
    log.info('Connect database')
    con = sqlite3.connect('.mwl-githut-data.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM data")
    languageServer = cur.fetchone()[14]
    cur.close()
    con.close()
    log.info('Closed database')
    if oscore == 'nt':
        cache = ['libs\\language-packages\\','\\']
    else:
        cache = ['libs/language-packages/','/']
    if not (os_path_isdir(cache[0] + language) and os_path_isfile(cache[0] + language + cache[1] + 'info.json') and os_path_isfile(cache[0] + language + cache[1] + 'all-language.json')):
        if languageServer[:8] == 'https://' or languageServer[:7] == 'http://':
            def deleteNew(cache:str) -> None:
                if not os_path_isdir(cache):
                    if os_path_isfile(cache):
                        os_remove(cache)
                        log.info("language.switchLanguage: 200, Delete '{}' file".format(cache))
                    os_mkdir(cache)
                    log.info("language.switchLanguage: 200, Create '{}' dir".format(cache))
            # Get JSON
            try:
                cache = requests_get(languageServer + '/language-package-links.json').text
            except Exception:
                log.warning('language.switchLanguage: 400, Could\'t request language server')
                return {'code':400,'message':'Could\'t request language server'}
            log.info('language.switchLanguage: 200, Got JSON')
            # Load JSON
            try:
                cache = json_loads(cache)
            except Exception:
                log.warning('language.switchLanguage: 400, Could\'t load JSON')
                return {'code':400,'message':'Could\'t load JSON'}
            log.info('language.switchLanguage: 200, Loaded JSON')
            # Find Language Package
            try:
                cache = cache[language]
            except Exception:
                log.warning('language.switchLanguage: 400, Could\'t find language package')
                return {'code':400,'message':'Could\'t find language package'}
            # Get Language Package
            languagePackage = []
            try:
                languagePackage.append(requests_get(cache + '/info.json').text)
                languagePackage.append(requests_get(cache + '/all-language.json').text)
            except Exception:
                log.warning('language.switchLanguage: 400, Could\'t get language package')
                return {'code':400,'message':'Could\'t get language package'}
            if not os_path_exists('libs') and os_path_isfile('libs'):
                os_remove('libs')
                log.info("language.switchLanguage: 200, Delete 'libs' file")
            if not os_path_isdir('libs'):
                os_mkdir('libs')
                log.info("language.switchLanguage: 200, Create 'libs' dir")
            if oscore == 'nt':
                cache = 'libs\\language-packages'
            else:
                cache = 'libs/language-packages'
                deleteNew(cache)
            if oscore == 'nt':
                cache = 'libs\\language-packages\\'
            else:
                cache = 'libs/language-packages/'
                deleteNew(cache)
            cache += language
            deleteNew(cache)
            if oscore == 'nt':
                cache += '\\'
            else:
                cache += '/'
            file = open(cache + 'info.json','w')
            file.write(languagePackage[0])
            file.close()
            file = open(cache + 'all-language.json','w')
            file.write(languagePackage[1])
            file.close()
        else:
            cur.close()
            con.close()
            log.info('Closed database')
            return {'code':400,'message':'Please enter a HTTP/HTTPS link'}
    con = sqlite3.connect('.mwl-githut-data.db')
    log.info('Connected to database')
    cur = con.cursor()
    if update == 0:
        cur.execute("UPDATE data SET language='{}' WHERE id=1".format(language))
        con.commit()
    cur.close()
    con.close()
    log.info('Closed database')
    return {'code':200,'message':'Updated language'}
# Language Class
class languageC():
    "Language class for main core, please use reload function to load language first, won't auto load"
    def reload(self,otherLanguage:bool=False,broken:bool=False,jsonDict:dict={},infoDict:dict={}) -> None:
        """Main core(githut_core.py)'s language reload function
Use globalLanguage to get parameter first."""
        if otherLanguage:
            self.languagePackageInformation = [infoDict['name'],infoDict['date'],infoDict['author'],'No',infoDict['website'],infoDict['language']]
            self.aboutPMT = jsonDict['aboutPMT']
            self.aboutPMTgtv = jsonDict['aboutPMTgtv']
            self.aboutPMTpgv = jsonDict['aboutPMTpgv']
            self.aboutPMTpyv = jsonDict['aboutPMTpyv']
            self.aboutPMTgithub = jsonDict['aboutPMTgithub']
            self.aboutAMT = jsonDict['aboutAMT']
            self.aboutAMTauthor = jsonDict['aboutAMTauthor']
            self.aboutAMTmainD = jsonDict['aboutAMTmainD']
            self.aboutAMTverN = jsonDict['aboutAMTverN']
            self.aboutAMTblog = jsonDict['aboutAMTblog']
            self.githutH = linesText(jsonDict['githutH'])
            self.help = linesText(jsonDict['help'])
            self.peToken = jsonDict['peToken']
            self.hToken = jsonDict['hToken']
            self.nhToken = jsonDict['nhToken']
            self.configH = linesText(jsonDict['configH'])
            self.licenseE = jsonDict['licenseE']
            self.terror = jsonDict['terror']
            self.loginS = jsonDict['loginS']
            self.loginSU = jsonDict['loginSU']
            self.Lname = jsonDict['Lname']
            self.alY = jsonDict['alY']
            self.alN = jsonDict['alN']
            self.NalY = jsonDict['NalY']
            self.NalN = jsonDict['NalN']
            self.alogin = jsonDict['alogin']
            self.rdata = jsonDict['rdata']
            self.adata = jsonDict['adata']
            self.errorInfo = jsonDict['errorInfo']
            self.ploginT = jsonDict['ploginT']
            self.cerror = jsonDict['cerror']
            self.notc = jsonDict['notc']
            self.createH = linesText(jsonDict['createH'])
            self.crepoE = jsonDict['crepoE']
            self.crepoS = jsonDict['crepoS']
            self.drepoE = jsonDict['drepoE']
            self.drepoS = jsonDict['drepoS']
            self.dmY = jsonDict['dmY']
            self.dmN = jsonDict['dmN']
            self.NdmY = jsonDict['NdmY']
            self.NdmN = jsonDict['NdmN']
            self.deleteH = linesText(jsonDict['deleteH'])
            self.couldtGetFeedbackServerInfo = jsonDict['couldtGetFeedbackServerInfo']
            self.feedbackServerClose = jsonDict['feedbackServerClose']
            self.notSupportIPv6 = jsonDict['notSupportIPv6']
            self.feedbackGetAdmin = jsonDict['feedbackGetAdmin']
            self.feedbackGetPassword = jsonDict['feedbackGetPassword']
            self.couldtLogin = jsonDict['couldtLogin']
            self.loginSuccess = jsonDict['loginSuccess']
            self.passwordError = jsonDict['passwordError']
            self.userNotFound = jsonDict['userNotFound']
            self.serverError = jsonDict['serverError']
            self.unknownError = jsonDict['unknownError']
            self.feedbackType = jsonDict['feedbackType']
            self.feedbackInfo = jsonDict['feedbackInfo'] + '\n'
            self.couldtFeedback = jsonDict['couldtFeedback'] + '"'
            self.feedbackSuccess = jsonDict['feedbackSuccess']
            self.blocked = jsonDict['blocked']
            self.ctY = jsonDict['ctY']
            self.ctN = jsonDict['ctN']
            self.NctY = jsonDict['NctY']
            self.NctN = jsonDict['NctN']
            self.acuY = jsonDict['acuY']
            self.acuN = jsonDict['acuN']
            self.NacuY = jsonDict['NacuY']
            self.NacuN = jsonDict['NacuN']
            self.couldtNotice = jsonDict['couldtNotice']
            self.noticeLvN = jsonDict['noticeLvN']
            self.noticeLvU = jsonDict['noticeLvU']
            self.noticeLv0 = jsonDict['noticeLv0']
            self.noticeLv1 = jsonDict['noticeLv1']
            self.noticeLv2 = jsonDict['noticeLv2']
            self.noticeLv3 = jsonDict['noticeLv3']
        else:
            self.languagePackageInformation = ['GitHub Tools English Language Package','2022-07-20','MacWinLin Studio CGK Team','No','githut.macwinlin.ml','en-us']
            if broken:
                self.languagePackageInformation[3] = 'Yes'
            # About Program Part
            self.aboutPMT = 'About Program'
            self.aboutPMTgtv = 'Version:alpha 0.2'
            self.aboutPMTpgv = 'PyGithub Version:1.55'
            self.aboutPMTpyv = 'Last Test Python Version:3.9.1'
            self.aboutPMTgithub = 'Open GitHub Repository,Please Use githut -po'
            # About Author Part
            self.aboutAMT = 'About Author'
            self.aboutAMTauthor = 'Author:MacWinLin Studio'
            self.aboutAMTmainD = 'Main Developer:Xinxin2021'
            self.aboutAMTverN = 'Version Updated Time:May 21, 2022'
            self.aboutAMTblog = 'Open MWL Studio\'s Blog,Please Use githut -am'
            # Githut Helper Text
            self.githutH = '''You can use these command:
-a | --author          About Author
-ao | --author-open    Open MacWinLin Studio's Blog
-p | --program         About Program
-po | --program-open   Open GitHub Repository
-l | --license         See This Project's License
-c | --copyright       See This Project's Copyright'''
            # Global Helper Text
            self.help = '''You can use these command:
help      Helper
githut    About
config    Config Information
login     Login GitHub Account
redata    Rebuild Database
backup    Backup Database
create    Create Any
import    Import Backup
feedback  Feedback to MWL CGK Team'''
            # About Token Text
            self.peToken = 'Please enter token!'
            self.hToken = 'Please delete the token first.'
            self.nhToken = 'Please add the token first.'
            self.configH = '''You can use these command:
language <language>                   Change GithuT Language
token [add | remove] <github-token>   Change GitHub Token
autologin [-y/--yes | -n/--no]        Enable/Disable Autologin
develop [-y/--yes | -n/--no]          Enable/Disable Develop Mode
feedback <link>                       Change Feedback Server Link
ct [-y/--yes | -n/--no]               Clear Token In Exit Program
update [-y/--yes | -n/--no]           Enable/Disable Auto Check Update
UPS <link>                            Change Update Server
LPS <link>                            Change Language Package Server'''
            self.licenseE = 'Could\'t load license,please confirm you connect the network.'
            # Login
            self.terror = 'Could\'t login,please confirm your token is right!'
            self.loginS = 'Login successful!'
            self.loginSU = 'Username:'
            self.Lname = '.Name:'
            # Autologin
            self.alY = 'Autologin is enable now!'
            self.alN = 'Autologin is disable now!'
            self.NalY = 'Please disable autologin first!'
            self.NalN = 'Please enable autologin first!'
            self.alogin = 'Autologin started!'
            # Rebuild Database
            self.rdata = 'Removed database file!'
            self.adata = 'Rebuilded database!'
            # All
            self.errorInfo = 'Error Info:'
            self.ploginT = 'Please login first!'
            self.cerror = 'Command error.'
            self.notc = ' is not a command.'
            # Create
            self.createH = '''You can use these command:
repo <RepoName>    Create GitHub Repository'''
            # =Repo
            self.crepoE = 'Could\'t create repository.'
            self.crepoS = 'The repository was created successfully!'
            # Develop Mode
            self.dmY = 'Develop mode is enable now!'
            self.dmN = 'Develop mode is disable now!'
            self.NdmY = 'Please disable develop mode first!'
            self.NdmN = 'Please enable develop mode first!'
            # Delete
            self.deleteH = '''You can use these command:
repo <RepoName>    Delete GitHub Repository'''
            # =Repo
            self.drepoE = 'Could\'t delete repository.'
            self.drepoS = 'The repository was deleted successfully!'
            # Feedback
            self.couldtGetFeedbackServerInfo = 'Could\'t get feedback server information.'
            self.feedbackServerClose = 'Feedback server is closed.'
            self.notSupportIPv6 = 'Your computer not support IPv6.'
            self.feedbackGetAdmin = 'Please enter your feedback username:'
            self.feedbackGetPassword = 'Please enter your feedback passowrd:'
            self.couldtLogin = 'Could\'t login.'
            self.loginSuccess = 'Login successful.'
            self.passwordError = 'Password error,please enter right password.'
            self.userNotFound = 'This user is not exist.'
            self.serverError = 'Feedback server error.'
            self.unknownError = 'Unknown error.'
            self.feedbackType = 'Please select feedback type(bug/warn/debug):'
            self.feedbackInfo = 'Please enter feedback info(alone enter ":w" to exit):\n'
            self.couldtFeedback = 'Could\'t feedback to "'
            self.feedbackSuccess = 'Feedback successful.'
            self.blocked = 'Your feedback account was blocked.'
            # Clear Token
            self.ctY = 'Clear token is enable now!'
            self.ctN = 'Clear token is disable now!'
            self.NctY = 'Please disable clear token first!'
            self.NctN = 'Please enable clear token first!'
            # Auto Check Update
            self.acuY = 'Auto check update is enable now!'
            self.acuN = 'Auto check update is disable now!'
            self.NacuY = 'Please disable auto check update first!'
            self.NacuN = 'Please enable auto check update first!'
            # Notice
            self.couldtNotice = 'Could\'t get notice.'
            self.noticeLvN = 'Null level notice:'
            self.noticeLvU = 'Unknown level notice:'
            self.noticeLv0 = 'Level 0 notice:'
            self.noticeLv1 = 'Level 1 notice:'
            self.noticeLv2 = 'Level 2 notice:'
            self.noticeLv3 = 'Level 3 notice:'
class BackupLanguage():
    "Language class for backup core, please use reload function to load language first, won't auto load"
    def reload(self,otherLanguage:bool=False,broken:bool=False,jsonDict:dict={},infoDict:dict={}) -> None:
        """Backup core(backup_core.py)'s language reload function
Use globalLanguage(type:backup) to get parameter first"""
        if otherLanguage:
            self.languagePackageInformation = [infoDict['name'],infoDict['date'],infoDict['author'],'No',infoDict['website'],infoDict['language']]
            self.replace = jsonDict['replace']
            self.replaceE = jsonDict['replaceE']
            self.filename = jsonDict['filename']
            self.errorInfo = jsonDict['errorInfo']
            self.openE = jsonDict['openE']
            self.path = jsonDict['path']
            self.path_windows = jsonDict['path_windows'] + 'D:\\GithuT\\backup-2022-7-19-304885.backup)'
            self.pathE = jsonDict['pathE']
            self.isBackup = jsonDict['isBackup']
            self.structrue = jsonDict['structrue']
            self.itCanUse = jsonDict['itCanUse']
            self.backupC = jsonDict['backupC']
            self.canOpen = jsonDict['canOpen']
            self.cantOpen = jsonDict['cantOpen']
            self.numberE = jsonDict['numberE']
            self.structrueE = jsonDict['structrueE']
            self.sha256E = jsonDict['sha256E']
            self.jsonE = jsonDict['jsonE']
            self.json = jsonDict['json']
            self.readE = jsonDict['readE']
            self.read = jsonDict['read']
            self.verE = jsonDict['verE']
            self.ver = jsonDict['ver']
            self.importS = jsonDict['importS']
            self.importE = jsonDict['importE']
            self.lenE = jsonDict['lenE']
        else:
            self.languagePackageInformation = ['GitHub Tools English Language Package','2022-07-20','MacWinLin Studio CGK Team','No','githut.macwinlin.ml','en-us']
            if broken:
                self.languagePackageInformation[3] = 'Yes'
            self.replace = 'Do you want to replace the previous?(y/n)'
            self.replaceE = 'Please enter right option!'
            self.filename = 'Save successfully.File:'
            self.errorInfo = 'Error Info:'
            self.openE = 'Open backup file error!'
            self.path = 'Please enter backup file path:(e.g. /home/githut/GithuT/backup-2022-4-23-305931.backup)'
            self.pathE = 'Path error,please enter right path!'
            self.backupC = 'Backup was cancelled.'
            self.canOpen = '√  The backup file can open.'
            self.cantOpen = '×  The backup file could\'t open.'
            self.isBackup = '√  It\'s a backup file.'
            self.structrue = '√  The backup file structure is correct.'
            self.itCanUse = '√  It have backup datas.'
            self.numberE = '×  Its file number not is two.'
            self.structrueE = '×  The backup file structrue error.'
            self.sha256E = '×  Could\'t verify backup file.'
            self.jsonE = '×  Could\'t load backup datas.'
            self.json = '√  Loaded backup datas.'
            self.readE = '×  Could\'t read datas.'
            self.read = '√  Read backup datas.'
            self.verE = '×  Backup file version is low.'
            self.ver = '√  Support this backup file version.'
            self.importS = '√  Imported backup file to database.'
            self.importE = '×  Could\'t import backup file to database.'
            self.lenE = '×  Backup file data number is big/small.'
class UpdateLanguage():
    "Language class for update program, please use reload function to load language first, won't auto load"
    def reload(self,otherLanguage:bool=False,broken:bool=False,jsonDict:dict={},infoDict:dict={}) -> None:
        """Update program(in shell.py)'s language reload function
Use globalLanguage(type:update) to get parameter first"""
        if otherLanguage:
            self.languagePackageInformation = [infoDict['name'],infoDict['date'],infoDict['author'],'No',infoDict['website'],infoDict['language']]
            self.haveNew = jsonDict['haveNew']
            self.downloadE = jsonDict['downloadE']
            self.updateLanguage = jsonDict['updateLanguage']
            self.browseDownload = jsonDict['browseDownload']
        else:
            self.languagePackageInformation = ['GitHub Tools English Language Package','2022-07-20','MacWinLin Studio CGK Team','No','githut.macwinlin.ml','en-us']
            if broken:
                self.languagePackageInformation[3] = 'Yes'
            self.haveNew = 'Have new version,is it install?(y/n)'
            self.downloadE = 'Could\'t get update.'
            self.updateLanguage = 'Updating language package...'
            self.browseDownload = '[INFO]Please browse githut.macwinlin.ml to download language package'
class globalLanguage():
    "Global language class, please to get parameter, won't auto return"
    def reload(self,languageType: str='main') -> list:
        "Before use others language class, please use this reload function to get a parameter list."
        def returnEnglish(broken:bool=False):
            log.info('language.global: Return English package')
            if broken:
                return [False,True,{},{}]
            else:
                return [False,False,{},{}]
        language = readLanguage()
        if language == 'en-us':
            return returnEnglish()
        if oscore == 'nt':
            cache = 'libs\\language-packages\\'
        else:
            cache = 'libs/language-packages/'
        if not os_path_isdir(cache):
            return returnEnglish()
        elif not os_path_isdir(cache + language):
            con = sqlite3.connect('.mwl-githut-data.db')
            log.info('language.global: Connected to database')
            cur = con.cursor()
            cur.execute("UPDATE data SET language='en-us' WHERE id=1")
            con.commit()
            cur.close()
            con.close()
            log.info('language.global: Closed database')
            return returnEnglish()
        else:
            cache += language
            if oscore == 'nt':
                cache += '\\'
            else:
                cache += '/'
            if not os_path_isfile(cache + 'info.json') and os_path_isfile(cache + 'all-langauge.json'):
                log.warning('language.global: Could\'t load ')
                return returnEnglish(True)
            else:
                file = open(cache + 'info.json','r')
                infoDictText = file.read()
                file.close()
                file = open(cache + 'all-language.json','r')
                jsonDictText = file.read()
                file.close()
                try:
                    jsonDict = json_loads(jsonDictText)
                    infoDict = json_loads(infoDictText)
                except Exception:
                    log.warning('language.global: Could\'t loads language package\s JSON file')
                    return returnEnglish(True)
                else:
                    if languageType == 'backup':
                        jsonDict = jsonDict['backup']
                    elif languageType == 'update':
                        jsonDict = jsonDict['update']
                    else:
                        jsonDict = jsonDict['main']
                    return [True,False,jsonDict,infoDict]