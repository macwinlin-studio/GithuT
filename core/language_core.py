# coding=utf-8
import sqlite3
from os.path import isfile as os_path_isfile
from locale import getdefaultlocale as getlanguage
from platform import platform
from os import popen as os_popen
# project: GitHub Tools Language Core
# file: language_core.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: LTS(Long Term Support) 1.0
# Publish only on GitHub and MacWinLin Studio's GitLab.
# Copyright 2022 MacWinLin Studio.All rights reserved.

# Code

# Def Create Databese
def cdatabase():
    con = sqlite3.connect('.mwl-githut-data.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY,language TEXT NOT NULL DEFAULT 'en-us',htoken INTEGER DEFAULT 0,token TEXT,alogin INTEGER NOT NULL DEFAULT 0,gmode INTEGER NOT NULL DEFAULT 0)")
    cur.execute("INSERT INTO data values (1,'en-us',0,'123456',0,0)")
    con.commit()
    # Change Default Language,Only Support Simplified Chinese,Can Add
    if 'zh' in getlanguage()[0]:
        cur.execute("UPDATE data SET language='zh-cn' WHERE id=1")
        con.commit()
    cur.close()
    con.close()
    if 'Windows' in platform():
        os_popen('attrib +H .mwl-githut-data.db')
# Create Database
if not os_path_isfile('.mwl-githut-data.db'):
    cdatabase()
# Language Function
class languageC():
    def __init__(self):
        # Add Language Please Change This List
        self.lList = ['zh-cn','en-us']
        # Language Module Won't Load Language,Please Use Reload Function To Load Language
    def readLanguage():
        con = sqlite3.connect('.mwl-githut-data.db')
        cur = con.cursor()
        cur.execute('select * from data')
        cache = cur.fetchone()
        cur.close()
        con.close()
        return cache[1]
    def reload(self):
        if languageC.readLanguage() == 'zh-cn':
            self.aboutPMT = '关于程序'
            self.aboutPMTgtv = '版本:LTS(长期支持)1.0'
            self.aboutPMTpgv = 'PyGithub版本:1.55'
            self.aboutPMTpyv = '上次测试Python版本:3.9.1'
            self.aboutPMTgithub = '打开GitHub仓库,请使用githut -po'
            self.aboutAMT = '关于作者'
            self.aboutAMTauthor = '作者:MacWinLin工作室'
            self.aboutAMTmainD = '主开发者:Xinxin2021'
            self.aboutAMTverN = '版本更新时间:2022年3月26日'
            self.aboutAMTblog = '打开MWL工作室博客,请使用githut -ao'
            self.githutH = '''您可以使用这些命令：
-a | --author    关于作者
-ao | --author-open    打开MacWinLin工作室博客
-p | --program    关于程序
-po | --program-open 打开GitHub仓库
-l | --license    查看开源协议
-c | --copyright    查看版权信息'''
            self.help = '''你可以使用这些命令：
help      帮助
githut    关于
config    配置信息
login     登录
redata    重新生成数据库'''
            self.hToken = '请先删除Token。'
            self.nhToken = '请先添加Token。'
            self.configH = '''您可以使用这些命令：
language <language>                   更改GithuT语言
token <github-token>              更改GitHub Token
autologin [-y/--yes | -n/--no     更改自动登录状态
git [-y/--yes | -n/--no]          更改Git模式状态'''
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
            self.crepoE = '新建仓库失败。'
            self.crepoS = '仓库新建成功！'
            self.gmodeY = 'Git模式已启用！'
            self.gmodeN = 'Git模式已禁用！'
            self.NgmodeY = '请先禁用Git模式！'
            self.NgmodeN = '请先启用Git模式！'
        else:
            # About Program Part
            self.aboutPMT = 'About Program'
            self.aboutPMTgtv = 'Version:LTS(Long Term Support) 1.0'
            self.aboutPMTpgv = 'PyGithub Version:1.55'
            self.aboutPMTpyv = 'Last Test Python Version:3.9.1'
            self.aboutPMTgithub = 'Open GitHub Repository,Please Use githut -po'
            # About Author Part
            self.aboutAMT = 'About Author'
            self.aboutAMTauthor = 'Author:MacWinLin Studio'
            self.aboutAMTmainD = 'Main Developer:Xinxin2021'
            self.aboutAMTverN = 'Version Updated Time:March 26, 2022'
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
redata    Rebuild Database'''
            # About Token Text
            self.hToken = 'Please delete the token first.'
            self.nhToken = 'Please add the token first.'
            self.configH = '''You can use these command:
language <language>               Change GithuT Language
token <github-token>              Change GitHub Token
autologin [-y/--yes | -n/--no]    Change Autologin State
git [-y/--yes | -n/--no]          Change Git Mode State'''
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
            # Repo
            self.crepoE = 'Could\'t create repository.'
            self.crepoS = 'The repository was created successfully!'
            # Git Mode
            self.gmodeY = 'Git mode is enable now!'
            self.gmodeN = 'Git mode is disable now!'
            self.NgmodeY = 'Please disable git mode now!'
            self.NgmodeN = 'Please enable git mode now!'