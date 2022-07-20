# coding=utf-8
from zipfile import ZipFile
from os import rename
from os.path import isfile
from sys import exit as sys_exit
if not isfile('info.json') and isfile('all-language.json'):
    print('[ERROR]No info.json and all-language.json')
    sys_exit()
# ZIP File
with ZipFile('language-package.zip','w') as z:
    z.write('info.json')
    z.write('all-language.json')
print('[INFO]Genreate ZIP File')
rename('language-package.zip','language-package.lpac')
print('[SUCCESS]Generage LPAC File')