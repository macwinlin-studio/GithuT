# coding=utf-8
# project: GitHub Tools Shell
# file: shell.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: LTS(Long Term Support) 1.0
# Publish only on GitHub and MacWinLin Studio's GitLab.
# Copyright 2022 MacWinLin Studio.All rights reserved.
# Make unofficial GUI client please view core file.
print('Github Tools Shell 1.0')
print(''' GitHub GitHub GitHub GitHub GitHub GitHub GitHub 
T-----=-----  --------    ---------   |           T
O     |      =        =  =         =  |           O
O     |     |          ||           | |           O
T     |     |          ||           | |           L
T     |     |          ||           | |           T
O     |     |          ||           | |           O
O     |      =        =  =         =  |           O
L     |       --------    ---------   =---------  L
 MacWinLin MacWinLin MacWinLin MacWinLin MacWinLin ''')
from core.githut_core import run
def main(state=0):
    if state == 0:
        while True:
            tml = input('>')
            run(tml)
main()
