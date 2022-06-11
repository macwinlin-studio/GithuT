# coding=utf-8
import sqlite3
from os.path import isfile as os_path_isfile
from os.path import isdir as os_path_isdir
from os import rmdir as os_rmdir
from locale import getdefaultlocale as getlanguage
from platform import platform
from os import popen as os_popen
# project: GitHub Tools Language Core
# file: language_core.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: 22w24b
# Publish only on GitHub and MacWinLin Studio's GitLab.
# Copyright 2022 MacWinLin Studio.All rights reserved.

# Code

# Define Read Language
def readLanguage():
        con = sqlite3.connect('.mwl-githut-data.db')
        cur = con.cursor()
        cur.execute('select * from data')
        cache = cur.fetchone()
        cur.close()
        con.close()
        return cache[1]
# Define Create Databese
def cdatabase():
    con = sqlite3.connect('.mwl-githut-data.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY,language TEXT NOT NULL DEFAULT 'en-us',htoken INTEGER NOT NULL DEFAULT 0,token TEXT,alogin INTEGER NOT NULL DEFAULT 0,developM INTEGER NOT NULL DEFAULT 0,version TEXT NOT NULL DEFAULT 'a0.2-22w24b',updateT INTEGER NOT NULL DEFAULT 1,feedback INTEGER NOT NULL DEFAULT 0,feedback_admin TEXT,feedback_link TEXT NOT NULL DEFAULT 'https://githut.macwinlin.ml/feedback.json',clearToken INTEGER NOT NULL DEFAULT 0,ups TEXT NOT NULL DEFAULT 'https://githut.macwinlin.ml/update',debug INTEGER NOT NULL DEFAULT 0)")
    cur.execute("INSERT INTO data values (1,'en-us',0,'123456',0,0,'a0.2-22w24b',1,0,'123456','https://githut.macwinlin.ml',0,'https://githut.macwinlin.ml/update',0)")
    con.commit()
    # Change Default Language,Only Support Simplified Chinese,Can Add
    if 'zh' in getlanguage()[0]:
        cur.execute("UPDATE data SET language='zh-cn' WHERE id=1")
        con.commit()
    cur.close()
    con.close()
    if 'Windows' in platform():
        os_popen('attrib +H .mwl-githut-data.db')
# Define Read Database
def rdatabase():
    return ['id','language','htoken','token','alogin','developM','version','updateT','feedback','feedback_admin']
# Create Database
if not os_path_isfile('.mwl-githut-data.db'):
    if os_path_isdir('.mwl-githut-data.db'):
        os_rmdir('.mwl-githut-data.db')
    cdatabase()
# Language Function
class languageC():
    def __init__(self):
        # Add Language Please Change This List
        # Language Module Won't Load Language,Please Use Reload Function To Load Language
        self.lList = ['zh-cn','en-us']
    def reload(self):
        if readLanguage() == 'zh-cn':
            self.aboutPMT = '关于程序'
            self.aboutPMTgtv = '版本:alpha 0.2'
            self.aboutPMTpgv = 'PyGithub版本:1.55'
            self.aboutPMTpyv = '上次测试Python版本:3.9.1'
            self.aboutPMTgithub = '打开GitHub仓库,请使用githut -po'
            self.aboutAMT = '关于作者'
            self.aboutAMTauthor = '作者:MacWinLin工作室'
            self.aboutAMTmainD = '主开发者:Xinxin2021'
            self.aboutAMTverN = '版本更新时间:2022年5月21日'
            self.aboutAMTblog = '打开MWL工作室博客,请使用githut -ao'
            self.githutH = '''您可以使用这些命令：
-a | --author          关于作者
-ao | --author-open    打开MacWinLin工作室博客
-p | --program         关于程序
-po | --program-open   打开GitHub仓库
-l | --license         查看开源协议
-c | --copyright       查看版权信息'''
            self.help = '''你可以使用这些命令：
help      帮助
githut    关于
config    配置信息
login     登录
redata    重新生成数据库
backup    备份数据库
create    创建任何
import    导入备份
feedback  反馈至CGK团队'''
            self.peToken = '请输入Token！'
            self.hToken = '请先删除Token。'
            self.nhToken = '请先添加Token。'
            self.configH = '''您可以使用这些命令：
language <language>                   更改GithuT语言
token [add | remove] <github-token>   更改GitHub Token
autologin [-y/--yes | -n/--no]        启用/禁用自动登录
develop [-y/--yes | -n/--no]          启用/禁用开发模式
feedback <link>                       更改反馈服务器链接
ct [-y/--yes | -n/--no]               退出前清除Token
update [-y/--yes | -n/--no]           启用/禁用自动检查更新
UPS <link>                            更改更新服务器链接'''
            self.licenseE = '无法加载协议，请确认您连接到网络。'
            self.accountH = '''您可以使用这些命令：
-u | --user         设置账号类型为个人
-o | --organization 设置账号类型为组织'''
            self.iso = '账号类型已设置为组织。'
            self.isu = '账号类型已设置为个人。'
            self.terror = '无法登陆，请确认您的Token正确！'
            self.loginS = '登录成功！'
            self.loginSU = '用户名：'
            self.Lname = '。名称：'
            self.alY = '自动登录已启用！'
            self.alN = '自动登录已禁用！'
            self.NalY = '请先禁用自动登录！'
            self.NalN = '请先启用自动登录！'
            self.alogin = '开始自动登录！'
            self.rdata = '已删除数据库文件！'
            self.adata = '已重新生成数据库！'
            self.errorInfo = '错误信息：'
            self.ploginT = '请先登录！'
            self.cerror = '命令错误。'
            self.notc = '不是命令。'
            self.createH = '''您可以使用以下命令：
repo <RepoName>    创建GitHub仓库'''
            self.crepoE = '无法新建仓库！'
            self.crepoS = '仓库新建成功！'
            self.drepoE = '无法删除仓库！'
            self.drepoS = '仓库删除成功！'
            self.dmY = '开发模式已启用！'
            self.dmN = '开发模式已禁用！'
            self.NdmY = '请先禁用开发模式！'
            self.NdmN = '请先启用开发模式！'
            self.deleteH = '''您可以使用以下命令：
repo <RepoName>    删除GitHub仓库'''
            self.couldtGetFeedbackServerInfo = '无法获取反馈服务器信息。'
            self.feedbackServerClose = '反馈服务器已关闭。'
            self.notSupportIPv6 = '您的电脑不支持IPv6。'
            self.feedbackGetAdmin = '请输入您的反馈用户名：'
            self.feedbackGetPassword = '请输入您的反馈密码：'
            self.couldtLogin = '无法登录。'
            self.loginSuccess = '登录成功。'
            self.passwordError = '密码错误，请输入正确的密码。'
            self.userNotFound = '此用户不存在。'
            self.serverError = '反馈服务器错误。'
            self.unknownError = '未知错误。'
            self.feedbackType = '请选择反馈类型(bug/warn/debug)：'
            self.feedbackInfo = '请输入反馈信息(单独输入":w"以退出):\n'
            self.couldtFeedback = '无法反馈至"'
            self.feedbackSuccess = '反馈成功。'
            self.blocked = '您的反馈账号已被封禁。'
            self.ctY = '清除Token已启用！'
            self.ctN = '清除Token已禁用！'
            self.NctY = '请先禁用清除Token！'
            self.NctN = '请先启用清除Token！'
            self.acuY = '自动检查更新已启用！'
            self.acuN = '自动检查更新已禁用！'
            self.NacuY = '请先禁用自动检查更新！'
            self.NacuN = '请先启用自动检查更新！'
            self.debugY = '调试模式已启用！'
            self.debugN = '调试模式已禁用！'
            self.NdebugY = '请先禁用调试模式！'
            self.NdebugN = '请先启用调试模式！'
            self.couldtNotice = '无法获取公告。'
            self.noticeLvN = '空等级公告：'
            self.noticeLvU = '未知等级公告：'
            self.noticeLv0 = '0级公告：'
            self.noticeLv1 = '1级公告：'
            self.noticeLv2 = '2级公告：'
            self.noticeLv3 = '3级公告：'
        else:
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
debug [-y/--yes | -n/--no]            Enable/Disable Debug Mode'''
            self.licenseE = 'Could\'t load license,please confirm you connect the network.'
            self.accountH = '''You can use these command:
-u | --user           Set The Account Type To Individual
-o | --organization   Set The Account Type To Organization'''
            # Set Account Type
            self.iso = 'The Account Type Is Set To Organization.'
            self.isu = 'The Account Type Is Set To Individual.'
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
            # Debug Mode
            self.debugY = 'Debug mode is enable now!'
            self.debugN = 'Debug mode is disable now!'
            self.NdebugY = 'Please disable debug mode first!'
            self.NdebugN = 'Please enable debug mode first!'
            # Notice
            self.couldtNotice = 'Could\'t get notice.'
            self.noticeLvN = 'Null level notice:'
            self.noticeLvU = 'Unknown level notice:'
            self.noticeLv0 = 'Level 0 notice:'
            self.noticeLv1 = 'Level 1 notice:'
            self.noticeLv2 = 'Level 2 notice:'
            self.noticeLv3 = 'Level 3 notice:'
class BackupLanguage():
    def __init__(self):
        self.lList = ['zh-cn','en-us']
    def reload(self):
        if readLanguage() == 'zh-cn':
            self.replace = '你想覆盖原来的文件吗？(y/n)'
            self.replaceE = '请输入正确的选项！'
            self.filename = '保存成功。文件：'
            self.errorInfo = '错误信息：'
            self.openE = '打开备份文件错误！'
            self.path = '请输入备份文件路径：（示例：/home/githut/GithuT/backup-2022-4-23-305931.backup）'
            self.pathE = '路径错误，请输入正确的路径！'
            self.isBackup = '√  它是一个备份文件。'
            self.structrue = '√  备份文件结构正确。'
            self.itCanUse = '√  它有备份数据。'
            self.backupC = '备份已取消。'
            self.canOpen = '√  备份文件已打开。'
            self.cantOpen = '×  备份文件无法打开。'
            self.numberE = '×  它的文件数量不为2。'
            self.structrueE = '×  备份文件结构错误。'
            self.sha256E = '×  无法验证备份文件。'
            self.jsonE = '×  无法加载备份数据。'
            self.json = '√  加载备份数据。'
            self.readE = '×  无法读取数据。'
            self.read = '√  读取备份数据。'
            self.verE = '×  备份文件版本低。'
            self.ver = '√  支持这个备份文件版本。'
            self.importS = '√  导入备份文件至数据库。'
            self.importE = '×  无法导入备份文件至数据库。'
            self.lenE = '×  备份文件数据过大/过小。'
        else:
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
    def __init__(self):
        self.lList = ['zh-cn','en-us']
    def reload(self):
        if readLanguage() == 'zh-cn':
            self.haveNew = '有新版本，是否安装？(y/n)'
            self.downloadE = '无法获取更新。'
        else:
            self.haveNew = 'Have new version,is it install?(y/n)'
            self.downloadE = 'Could\'t get update.'
