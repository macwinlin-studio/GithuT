# coding=utf-8
import logging
# project: GitHub Tools Log Core
# file: log_core.py
# author: MacWinLin Studio CGK Team
# email: githut@macwinlin.ml
# version: LTS(Long Term Support) 1.0.1
# Publish only on GitHub and MacWinLIn Studio's GitLab.
# Copyright 2022 MacWinLIn Studio.All rights reserved.

# Code

def basic(debug=0):
    if debug == 1:
        logging.basicConfig(level=logging.DEBUG,filemode='a+',filename='githut-log.log',format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
    else:
        logging.basicConfig(level=logging.CRITICAL,filemode='a+',filename='githut-log.log',format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
def debug(e):
    logging.debug(str(e))
def info(e):
    logging.info(str(e))
def warning(e):
    logging.warning(str(e))
def error(e):
    logging.error(str(e))
def critical(e):
    logging.critical(str(e))
def exception(e):
    logging.exception(e)