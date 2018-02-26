#-*- coding=UTF-8 -*-
import json
import requests
import datetime
import os
import time
import datetime
from NewLog import NewLog
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymysql
pymysql.install_as_MySQLdb()
from rpyc import Service
from rpyc.utils.server import ThreadedServer

A = NewLog(print_level='info')

class WatService(Service):

    def exposed_get_detail_html(self,name):
        try:
            with open ('{}_detail.html'.format(name),'r') as f:
                str = f.read()
                A.info("Read Successful")
        except IOError:
                str = "Task doesn't exist or doesn't finish."
                A.warning("Read Failed")
        return str

    def exposed_get_summary_html(self,name):
        try:
            with open ('{}_summary.html'.format(name),'r') as f:
                str = f.read()
                A.info("Read Successful")
        except IOError:
                str = "Task doesn't exist or doesn't finish."
                A.warning("Read Failed")
        return str

    def exposed_get_openvas_html(self,name):
        try:
            with open ('{}_openvas.html'.format(name),'r') as f:
                str = f.read()
                A.info("Read Successful")
        except IOError:
                str = "Task doesn't exist or doesn't finish."
                A.warning("Read Failed")
        return str


if __name__=="__main__":
    s = ThreadedServer(WatService,port=8888,auto_register=False)
    s.start()

