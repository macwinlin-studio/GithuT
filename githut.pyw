# coding=utf-8
import github,wx,webbrowser,sqlite3,language,requests,platform
# project: Github Tools
# file: githut.pyw
# author: Xinxin(MacWinLin Studio's Project)
# email: xmailxin@gmail.com or xinxinmlx@163.com
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
        self.aboutAM = wx.MenuItem(parentMenu=self.mebA,id=1,text=language.aboutAM,kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU,self.aboutAMF,id=1)
        self.aboutPM = wx.MenuItem(parentMenu=self.mebA,id=2,text=language.aboutPM,kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU,self.aboutPMF,id=2)
        self.quitM = wx.MenuItem(parentMenu=self.mebQ,id=3,text=language.quitM,kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_MENU,self.quitMF,id=3)
        self.meb.Append(self.mebA,language.about)
        self.meb.Append(self.mebQ,language.quit)
        self.mebA.Append(self.aboutAM)
        self.mebA.Append(self.aboutPM)
        self.mebQ.Append(self.quitM)
        self.SetMenuBar(self.meb)
        self.Stbr = self.CreateStatusBar(3)
        self.SetStatusWidths([-1,-1,-1])
        self.SetStatusText(language.aboutPMTpgv,0)
        self.SetStatusText(language.aboutPMTwpv,1)
        self.SetStatusText(language.gtv,2)
        self.Bind(wx.EVT_CLOSE,self.quitMF)

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
        cache = 'Token:' + datas[2]
        self.token = wx.StaticText(parent=panel,id=5,label=cache)
        self.searchTC = wx.TextCtrl(parent=panel,id=6)
        self.search = wx.Button(parent=panel,id=7,label='Search')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.searchTC,proportion=1,flag=wx.EXPAND)
        hbox.Add(self.search,flag=wx.RIGHT)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.user,flag=wx.EXPAND)
        vbox.Add(self.token,flag=wx.EXPAND)
        vbox.Add(hbox,flag=wx.EXPAND)
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
        exit(0)
    def feedbackF(self,event):
        webbrowser.open_new('https://support.qq.com/products/378689')
app = wx.App()
frame = Login()
frame.Show()
app.MainLoop()