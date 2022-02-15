# coding=utf-8
import sqlite3,pathlib
# project: CGK System Language Module
# file: language.py
# author: Xinxin(MacWinLin Studio's Project)
# email: xmailxin@gmail.com or xinxinmlx@163.com
# version: LTS(Long Term Support) 1.0
# Publish only on Github.
# Copyright 2022 Xinxin2021(Github) and MacWinLin Studio.All rights reserved.
cache = pathlib.Path('D:\\mwl-githut-data.db')
if not cache.is_file():
    con = sqlite3.connect('D:\\mwl-githut-data.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY,language TEXT NOT NULL DEFAULT 'en-us',remember INTEGER DEFAULT 0,token TEXT)")
    cur.execute("INSERT INTO data values (1,'en-us',0,'123456')")
    con.commit()
    cur.close()
    con.close()
def readLanguage():
    con = sqlite3.connect('D:\\mwl-githut-data.db')
    cur = con.cursor()
    cur.execute('select * from data')
    cache = cur.fetchone()
    cur.close()
    con.close()
    return cache
if readLanguage() == 'zh-cn':
    aboutPMT = '关于程序'
    aboutPMTgtv = '版本:LTS(长期支持)1.0'
    aboutPMTpgv = 'PyGithub版本:1.55'
    aboutPMTwpv = 'wxPython版本:4.1.1'
    aboutPMTpyv = '上次测试Python版本:3.9.1'
    aboutPMTgithub = '打开Github存储库'
    aboutAMT = '关于作者'
    aboutAMTauthor = '作者:MacWinLin工作室'
    aboutAMTmainD = '主开发者:Xinxin2021'
    aboutAMTverN = '版本更新时间:2022年2月11日'
    aboutAMTblog = '打开MWL工作室博客'
    about = '关于'
    quit = '退出'
    aboutAM = '关于作者'
    aboutPM = '关于程序'
    quitM = '退出程序\tCtrl+Q'
    gtv = '版本:LTS 1.0'
    chooseT = '选择账户类型'
    personalT = '个人'
    organizationT = '组织'
    rememberT = '记住Token'
    loginT = '登录'
    errorL = '请输入正确的Token!'
    feedbackT = '反馈'
    feedbackT1 = '提建议'
    feedbackT2 = '提缺陷'
    feedbackT3 = '我想要'
    userT = '用户:'
else:
    aboutPMT = 'About Program'
    aboutPMTgtv = 'Version:Long Term Support 1.0'
    aboutPMTpgv = 'PyGithub Version:1.55'
    aboutPMTwpv = 'wxPython Version:4.1.1'
    aboutPMTpyv = 'Last Test Python Version:3.9.1'
    aboutPMTgithub = 'View Github Repository'
    aboutAMT = 'About Author'
    aboutAMTauthor = 'Author:MacWinLin Studio'
    aboutAMTmainD = 'Main Developer:Xinxin2021'
    aboutAMTverN = 'Version Update Time:February 11, 2022'
    aboutAMTblog = 'View MWL Studio Blog'
    about = 'About'
    quit = 'Quit'
    aboutAM = 'About Author'
    aboutPM = 'About Program'
    quitM = 'Quit Program\tCtrl+Q'
    gtv = 'Version:LTS 1.0'
    chooseT = 'Choose Account Type:'
    personalT = 'Personal'
    organizationT = 'Organization'
    rememberT = 'Remember Token'
    loginT = 'Login'
    errorL = 'Please enter right token!'
    feedbackT = 'Feedback'
    feedbackT1 = 'Make suggestions'
    feedbackT2 = 'Defect lifting'
    feedbackT3 = 'I want'
    userT = 'User:'