# coding=utf-8
# This project is very old,we will not repair this project's bugs.
import github,wx,webbrowser,sqlite3,language
# project: Github Tools Old GUI
# file: githut.pyw
# author: Xinxin(MacWinLin Studio's Project)
# email: githut@macwinlin.ml
# version: LTS(Long Term Support) 1.0.0
# Publish only on GitHub.
# Copyright 2022 Xinxin2021(GitHub) and MacWinLin Studio.All rights reserved.
login = 0
datas = []
def query():
    con = sqlite3.connect('D:\\mwl-githut-data.db')
    cur = con.cursor()
    cur.execute('select * from data')
    cache = cur.fetchone()
    cur.close()
    con.close()
    return cache
class Login(wx.Frame):
    def __init__(self):
        super().__init__(None,title='Githut',size=(500,320))
        panel = wx.Panel(parent=self)

        self.account_type = 0
        self.remember = 0
        if query()[2] == 1:
            self.remember = 1

        icon = wx.Icon('icon.ico',wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.meb = wx.MenuBar()
        self.mebA = wx.Menu()
        self.mebQ = wx.Menu()
        self.mebL = wx.Menu()
        self.aboutAM = wx.MenuItem(parentMenu=self.mebA,id=1,text=language.aboutAM,kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU,self.aboutAMF,id=1)
        self.aboutPM = wx.MenuItem(parentMenu=self.mebA,id=2,text=language.aboutPM,kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU,self.aboutPMF,id=2)
        self.quitM = wx.MenuItem(parentMenu=self.mebQ,id=3,text=language.quitM,kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU,self.quitMF,id=3)
        self.englishM = wx.MenuItem(parentMenu=self.mebL,id=13,text='English',kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU,self.englishMF,id=13)
        self.chineseM = wx.MenuItem(parentMenu=self.mebL,id=14,text='简体中文',kind=wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU,self.chineseMF,id=14)
        self.meb.Append(self.mebA,language.about)
        self.meb.Append(self.mebQ,language.quit)
        self.meb.Append(self.mebL,language.languageT)
        self.mebA.Append(self.aboutAM)
        self.mebA.Append(self.aboutPM)
        self.mebQ.Append(self.quitM)
        self.mebL.Append(self.englishM)
        self.mebL.Append(self.chineseM)
        self.SetMenuBar(self.meb)
        self.Stbr = self.CreateStatusBar(3)
        self.SetStatusWidths([-1,-1,-1])
        self.SetStatusText(language.aboutPMTpgv,0)
        self.SetStatusText(language.aboutPMTwpv,1)
        self.SetStatusText(language.gtv,2)
        self.Bind(wx.EVT_CLOSE,self.quitMF)
        if language.readLanguage() == 'zh-cn':
            self.chineseM.Check(True)
        else:
            self.englishM.Check(True)

        self.logo = wx.StaticBitmap(panel,4,wx.Image('favicon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.title = wx.StaticText(parent=panel,id=5,label='Github Tools')
        self.tokenT = wx.StaticText(parent=panel,id=6,label='Token:')
        self.token = wx.TextCtrl(parent=panel,id=7,style=wx.TE_PASSWORD)
        self.rem = wx.CheckBox(parent=panel,id=11,label=language.rememberT)
        if self.remember == 1:
            self.rem.SetValue(True)
            self.token.SetValue(query()[3])
        self.Bind(wx.EVT_CHECKBOX,self.remF,id=11)
        self.login = wx.Button(parent=panel,id=12,label=language.loginT)
        self.Bind(wx.EVT_BUTTON,self.loginF,self.login)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.tokenT,flag=wx.EXPAND)
        hbox1.Add(self.token,proportion=1,flag=wx.EXPAND)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.logo,flag=wx.CENTER)
        vbox.Add(self.title,flag=wx.CENTER)
        vbox.Add(hbox1,flag=wx.EXPAND)
        vbox.Add(self.rem,flag=wx.EXPAND)
        vbox.Add(self.login,flag=wx.EXPAND)
        panel.SetSizer(vbox)
    def aboutAMF(self,event):
        aboutAMA = wx.App()
        aboutAMF = aboutAMC()
        aboutAMF.Show()
        aboutAMA.MainLoop()
    def aboutPMF(self,event):
        aboutPMA = wx.App()
        aboutPMF = aboutPMC()
        aboutPMF.Show()
        aboutPMA.MainLoop()
    def quitMF(self,event):
        exit()
    def remF(self,event):
        if self.rem.GetValue():
            self.remember = 1
            con = sqlite3.connect('D:\\mwl-githut-data.db')
            cur = con.cursor()
            cur.execute('UPDATE data SET remember=1 WHERE id=1')
            con.commit()
            cur.execute('UPDATE data SET token=? WHERE id=?',(self.token.GetValue(),1))
            con.commit()
            cur.close()
            con.close()
        else:
            self.remember = 0
            con = sqlite3.connect('D:\\mwl-githut-data.db')
            cur = con.cursor()
            cur.execute('UPDATE data SET remember=0 WHERE id=1')
            con.commit()
            cur.close()
            con.close()
    def loginF(self,event):
        self.remember = 1
        con = sqlite3.connect('D:\\mwl-githut-data.db')
        cur = con.cursor()
        cur.execute('UPDATE data SET remember=1 WHERE id=1')
        con.commit()
        cur.execute('UPDATE data SET token=? WHERE id=?', (self.token.GetValue(), 1))
        con.commit()
        cur.close()
        con.close()
        global datas
        datas = ['',self.account_type,self.token.GetValue()]
        try:
            g = github.Github(login_or_token=datas[2])
            cache = g.get_user()
            datas[0] = cache.name
        except github.GithubException:
            dlg = wx.MessageDialog(None,language.errorL,'ERROR',wx.OK|wx.ICON_ERROR)
            if dlg.ShowModal() == wx.ID_OK:
                pass
        else:
            global login
            login = 1
            self.login.Disable()
            loginA = wx.App()
            loginC = Main()
            loginC.Show()
            loginA.MainLoop()
    def englishMF(self,event):
        con = sqlite3.connect('D:\\mwl-githut-data.db')
        cur = con.cursor()
        cur.execute("UPDATE data SET language='en-us' WHERE id=1")
        con.commit()
        cur.close()
        con.close()
        dlg = wx.MessageDialog(parent=None,message=language.textIT,caption=language.informationT,style=wx.OK|wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_OK:
            exit(0)
    def chineseMF(self,event):
        con = sqlite3.connect('D:\\mwl-githut-data.db')
        cur = con.cursor()
        cur.execute("UPDATE data SET language='zh-cn' WHERE id=1")
        con.commit()
        cur.close()
        con.close()
        dlg = wx.MessageDialog(parent=None,message=language.textIT,caption=language.informationT,style=wx.OK|wx.ICON_INFORMATION)
        if dlg.ShowModal() == wx.ID_OK:
            exit(0)
class aboutPMC(wx.Frame):
    def __init__(self):
        super().__init__(None,title=language.aboutPMT,size=(300,310))
        panel = wx.Panel(parent=self)
        icon = wx.Icon('icon.ico',wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.logo = wx.StaticBitmap(panel,1,wx.Image('favicon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.title = wx.StaticText(parent=panel,id=2,label='Github Tools')
        self.gtv = wx.StaticText(parent=panel,id=3,label=language.aboutPMTgtv)
        self.pgv = wx.StaticText(parent=panel,id=4,label=language.aboutPMTpgv)
        self.wpv = wx.StaticText(parent=panel,id=5,label=language.aboutPMTwpv)
        self.pyv = wx.StaticText(parent=panel,id=6,label=language.aboutPMTpyv)
        self.github = wx.Button(parent=panel,id=7,label=language.aboutPMTgithub)
        self.Bind(wx.EVT_BUTTON,self.githubF,self.github)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.logo,flag=wx.CENTER)
        vbox.Add(self.title,flag=wx.CENTER)
        vbox.Add(self.gtv,flag=wx.CENTER)
        vbox.Add(self.pgv,flag=wx.CENTER)
        vbox.Add(self.wpv,flag=wx.CENTER)
        vbox.Add(self.pyv,flag=wx.CENTER)
        vbox.Add(self.github,flag=wx.CENTER)
        panel.SetSizer(vbox)
    def githubF(self,event):
        webbrowser.open_new('https://github.com/macwinlin-studio/GithuT/tree/1.0.0')
class aboutAMC(wx.Frame):
    def __init__(self):
        super().__init__(None,title=language.aboutAMT,size=(300,290))
        panel = wx.Panel(parent=self)
        icon = wx.Icon('icon.ico',wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.logo = wx.StaticBitmap(panel,1,wx.Image('favicon.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.title = wx.StaticText(parent=panel,label='Github Tools')
        self.author = wx.StaticText(parent=panel,label=language.aboutAMTauthor)
        self.mainD = wx.StaticText(parent=panel,label=language.aboutAMTmainD)
        self.verN = wx.StaticText(parent=panel,label=language.aboutAMTverN)
        self.blog = wx.Button(parent=panel,label=language.aboutAMTblog)
        self.Bind(wx.EVT_BUTTON,self.blogF,self.blog)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.logo,flag=wx.CENTER)
        vbox.Add(self.title,flag=wx.CENTER)
        vbox.Add(self.author,flag=wx.CENTER)
        vbox.Add(self.mainD,flag=wx.CENTER)
        vbox.Add(self.verN,flag=wx.CENTER)
        vbox.Add(self.blog,flag=wx.CENTER)
        panel.SetSizer(vbox)
    def blogF(self,event):
        webbrowser.open_new('https://macwinlin.github.io')
class Main(wx.Frame):
    def __init__(self):
        super().__init__(None,title='Githut - ' + datas[0],size=(500,500))
        panel = wx.Panel(parent=self)

        icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.meb = wx.MenuBar()
        self.mebA = wx.Menu()
        self.mebQ = wx.Menu()
        self.aboutAM = wx.MenuItem(parentMenu=self.mebA, id=1, text=language.aboutAM, kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.aboutAMF, id=1)
        self.feedbackM = wx.MenuItem(parentMenu=self.mebA,id=6,text=language.feedbackT,kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU,self.feedbackF,id=6)
        self.aboutPM = wx.MenuItem(parentMenu=self.mebA, id=2, text=language.aboutPM, kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.aboutPMF, id=2)
        self.quitM = wx.MenuItem(parentMenu=self.mebQ, id=3, text=language.quitM, kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU, self.quitMF, id=3)
        self.meb.Append(self.mebA, language.about)
        self.meb.Append(self.mebQ, language.quit)
        self.mebA.Append(self.aboutAM)
        self.mebA.Append(self.aboutPM)
        self.mebA.Append(self.feedbackM)
        self.mebQ.Append(self.quitM)
        self.SetMenuBar(self.meb)
        self.Stbr = self.CreateStatusBar(3)
        self.SetStatusWidths([-1, -1, -1])
        self.SetStatusText(language.aboutPMTpgv, 0)
        self.SetStatusText(language.aboutPMTwpv, 1)
        self.SetStatusText(language.gtv, 2)
        self.Bind(wx.EVT_CLOSE, self.quitMF)

        cache = language.userT + datas[0]
        self.user = wx.StaticText(parent=panel,id=4,label=cache)
        self.space1 = wx.StaticText(parent=panel,id=19,label='                                           ')
        self.logOut = wx.Button(parent=panel,id=21,label=language.logOutT)
        self.space3 = wx.StaticText(parent=panel,id=22,label='                                           ')
        self.refresh = wx.Button(parent=panel,id=15,label=language.refreshT)
        cache = 'Token:' + datas[2]
        self.token = wx.StaticText(parent=panel,id=5,label=cache)
        self.show = wx.CheckBox(parent=panel,id=20,label=language.showT)
        self.show.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX,self.showF,id=20)
        self.searchTC = wx.TextCtrl(parent=panel,id=6)
        self.search = wx.Button(parent=panel,id=7,label=language.searchT)
        self.repo1 = wx.RadioButton(parent=panel,id=6,label='',style=wx.RB_GROUP)
        cache = None
        if True:
            cache = language.repositoryT
        else:
            cache = language.repositoriesT
        self.repot = wx.StaticText(parent=panel,id=14,label=cache)
        self.repo2 = wx.RadioButton(parent=panel,id=7,label='')
        self.repo3 = wx.RadioButton(parent=panel,id=8,label='')
        self.repo4 = wx.RadioButton(parent=panel,id=9,label='')
        self.repo5 = wx.RadioButton(parent=panel,id=10,label='')
        self.repo6 = wx.RadioButton(parent=panel,id=11,label='')
        self.repo7 = wx.RadioButton(parent=panel,id=12,label='')
        self.repo8 = wx.RadioButton(parent=panel,id=13,label='')
        self.space2 = wx.StaticText(parent=panel,id=18,label='                                            ')
        self.left = wx.Button(parent=panel,id=16,label=language.leftT)
        self.right = wx.Button(parent=panel,id=17,label=language.rightT)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.space1,proportion=1,flag=wx.CENTER)
        hbox.Add(self.refresh,flag=wx.RIGHT)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.searchTC,proportion=1,flag=wx.EXPAND)
        hbox1.Add(self.search,flag=wx.RIGHT)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.repo1,flag=wx.LEFT)
        hbox2.Add(self.repo2,flag=wx.EXPAND)
        hbox2.Add(self.repo3,flag=wx.CENTER)
        hbox2.Add(self.repo4,flag=wx.RIGHT)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(self.repo5,flag=wx.LEFT)
        hbox3.Add(self.repo6,flag=wx.EXPAND)
        hbox3.Add(self.repo7,flag=wx.CENTER)
        hbox3.Add(self.repo8,flag=wx.RIGHT)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(self.left,flag=wx.LEFT)
        hbox4.Add(self.space2,proportion=1,flag=wx.CENTER)
        hbox4.Add(self.right,flag=wx.RIGHT)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5.Add(self.user,flag=wx.LEFT)
        hbox5.Add(self.space3,proportion=1,flag=wx.CENTER)
        hbox5.Add(self.logOut,flag=wx.RIGHT)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox,flag=wx.EXPAND)
        vbox.Add(hbox5,flag=wx.EXPAND)
        vbox.Add(self.token,flag=wx.EXPAND)
        vbox.Add(self.show,flag=wx.EXPAND)
        vbox.Add(hbox1,flag=wx.EXPAND)
        vbox.Add(self.repot,flag=wx.CENTER)
        vbox.Add(hbox2,flag=wx.EXPAND)
        vbox.Add(hbox3,flag=wx.EXPAND)
        vbox.Add(hbox4,flag=wx.EXPAND)
        panel.SetSizer(vbox)
        self.Update()
    def aboutAMF(self,event):
        aboutAMA = wx.App()
        aboutAMF = aboutAMC()
        aboutAMF.Show()
        aboutAMA.MainLoop()
    def aboutPMF(self,event):
        aboutPMA = wx.App()
        aboutPMF = aboutPMC()
        aboutPMF.Show()
        aboutPMA.MainLoop()
    def quitMF(self,event):
        exit(0)
    def feedbackF(self,event):
        webbrowser.open_new('https://support.qq.com/products/378689')
    def showF(self,event):
        if self.show.GetValue():
            cache = 'Token:' + datas[2]
            self.token.SetLabelText(cache)
        else:
            cache = ''
            for i in range(len(datas[2])):
                cache += '*'
            cache = 'Token:' + cache
            self.token.SetLabelText(cache)
app = wx.App()
frame = Login()
frame.Show()
app.MainLoop()
