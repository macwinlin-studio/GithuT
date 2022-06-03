# coding=utf-8
import logging
def basic(debug=0):
    if debug == 0:
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