#-*- coding=UTF-8 -*-
import json
import requests
import datetime
import os
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymysql
pymysql.install_as_MySQLdb()
import rpyc
from rpyc import Service
from rpyc.utils.server import ThreadedServer


conn = pymysql.connect(host='127.0.0.1',user='developer',passwd='ddosapi',db='ssc',port=7801,charset="utf8",cursorclass=pymysql.cursors.DictCursor)



class WatService(Service):

    def exposed_set_scan_type(self,type):
        self.type = type


    def exposed_get_task(self):
        # type = nessus or openvas
        sql = "select id, website from scan_task_list where {}_status = 0 limit 1".format(self.type)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        if result:
            update = "update scan_task_list set {0}_status=1,{0}_start_time='{1}' where id = {2}".format(self.type,datetime.datetime.now(),result['id'])
            cur.execute(update)
        conn.commit()
        return result

    def exposed_get_running(self):
        sql = "select id, website from scan_task_list where {}_status = 1".format(self.type)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        if result:
            ret = []
            for i in result:
                name = "task_{}_{}".format(i['id'],i['website'])
                ret.append(name)
            conn.commit()
            return ret

    def exposed_update_status(self,id):
        sql = "update scan_task_list set {0}_status = 2,{0}_finish_time='{1}' where id = {2}".format(self.type,datetime.datetime.now(),id)
        cur = conn.cursor()
        count = cur.execute(sql)
        conn.commit()
        if count == 1:
            return True
        else:
            return False

    def exposed_insert(self,name,website):
        #先查有没有相同域名的正在扫或在待扫队列中
        check = "select id from scan_task_list where website='{}' and (nessus_status!=2 or openvas_status!=2)".format(website)
        cur = conn.cursor()
        result = cur.execute(check)
        conn.commit()
        #有
        if result:
            res = cur.fetchall()
            id = res[-1]['id']
            return "task_{}_{}".format(id, website)
        #没有
        else:
            sql = "insert into scan_task_list(taskname,website) values ('{0}','{1}');".format(name,website)
            cur = conn.cursor()
            count = cur.execute(sql)
            conn.commit()
            if count == 1:
                #select = "select max(id) from scan_task_list"
                select = "select id from scan_task_list where website='{}'".format(website)
                cur = conn.cursor()
                cur.execute(select)
                conn.commit()
                r =  cur.fetchall()
                if r:
                    id = r[-1]['id']
                    return "task_{}_{}".format(id,website)

    def exposed_check_status(self,id,website):
        sql = "select nessus_status,openvas_status from scan_task_list where id = {} and website='{}'".format(id,website)
        cur = conn.cursor()
        count = cur.execute(sql)
        conn.commit()
        if count:
            result = cur.fetchone()
            if result['nessus_status'] == 2 and result['openvas_status'] == 2:
                #返回报告连结
                c = rpyc.connect('127.0.0.1', 8888)
                result = c.root.get_html("task_{}_{}".format(id,website))
                c.close()
                return result
            else:
                return "The task_{}_{} is scanning".format(id,website)
        else:
            return "The task_{}_{} doesn't exist".format(id,website)

if __name__=="__main__":
    s = ThreadedServer(WatService,port=7777,auto_register=False)
    s.start()

