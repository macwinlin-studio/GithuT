# coding=utf-8
import sqlite3
from os import mkdir,name,popen,listdir
from os.path import exists
from json import dumps
def cdatabase():
    con = sqlite3.connect('.mwl-githut-up-data.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER PRIMARY KEY,orgName TEXT,version TEXT,domain TEXT NOT NULL DEFAULT 'http://127.0.0.1')")
    cur.execute("INSERT INTO data VALUES(1,'Unknown organization','1.0','http://127.0.0.1')")
    con.commit()
    cur.close()
    con.close()
    if name == 'nt':
        popen('attrib +H .mwl-githut-up-data.db')
print(r'''                                                                                                                                                            
                                                                                                                                                                                
    //   ) )                             /__  ___/       //   / /                                                //   ) )                                                ___    
   //        ( ) __  ___ / __              / /          //   / /  ___      ___   /  ___    __  ___  ___         ((         ___      __              ___       /_  /    //   ) ) 
  //  ____  / /   / /   //   ) ) //   / / / /          //   / / //   ) ) //   ) / //   ) )  / /   //___) )        \\     //___) ) //  ) ) ||  / / //___) )     / /    //   / /  
 //    / / / /   / /   //   / / //   / / / /          //   / / //___/ / //   / / //   / /  / /   //                 ) ) //       //       || / / //           / /    //   / /   
((____/ / / /   / /   //   / / ((___( ( / /          ((___/ / //       ((___/ / ((___( (  / /   ((____       ((___ / / ((____   //        ||/ / ((____       / /   (|(___/ /    ''')
while True:
    tml = input('root# ')
    if tml in ['?','help']:
        print('''You can use these commands:
init            Initialize Update Folder
generate        Generate Json File
domain <domain> Config Domain
org <orgName>   Config Organization Name
version <ver>   Config Software Version
''')
    elif tml[:6] == 'domain':
        cache = tml[7:]
        if cache[:7] == 'http://' or cache[:8] == 'https://':
            con = sqlite3.connect('.mwl-githut-up-data.db')
            cur = con.cursor()
            cur.execute("UPDATE data SET domain='{}' WHERE id=1".format(cache))
            con.commit()
            cur.close()
            con.close()
        else:
            print("Domain prefix should is 'http://' or 'https://'")
    elif tml[:3] == 'org':
        cache = tml[4:]
        con = sqlite3.connect('.mwl-githut-up-data.db')
        cur = con.cursor()
        cur.execute("UPDATE data SET orgName='{}' WHERE id=1".format(cache))
        con.commit()
        cur.close()
        con.close()
    elif tml == 'init':
        if not exists('update'):
            mkdir('update')
            if name == 'nt':
                mkdir(r'update\files')
            else:
                mkdir('update/files')
        else:
            print('"update" is exists.')
    elif tml == 'generate':
        if exists('update'):
            if name == 'nt':
                file = open(r'update\latest.json','w')
                pathCache = r'update\files' + '\\'
            else:
                file = open('update/latest.json','w')
                pathCache = 'update/files/'
            con = sqlite3.connect('.mwl-githut-up-data.db')
            cur = con.cursor()
            cur.execute('SELECT * FROM data')
            cache = cur.fetchone()
            cur.close()
            con.close()
            jsonCache = {'org':cache[1],'latest':cache[2],'link':cache[3] + '/files/','files':listdir(pathCache)}
            file.write(dumps(jsonCache))
            file.close()
        else:
            print('Please initialize first.')
    else:
        print('Command error!')