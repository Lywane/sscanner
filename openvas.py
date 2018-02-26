# -*- coding: utf-8 -*-
from lxml import etree
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import rpyc
import requests
from NewLog import NewLog
import json
import ssl
import commands
ssl._create_default_https_context = ssl._create_unverified_context
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import base64
# Create your views here.

class OpenVas():

    def __init__(self,user,passwd):
        self.user = user
        self.passwd = passwd
        self.cmd_prefix = "omp -u {} -w {} --xml=".format(self.user,self.passwd)

    def exec_omp(self,cmd):
        ompcmd = "{}'{}'".format(self.cmd_prefix,cmd)
        status, output = commands.getstatusoutput(ompcmd)
        return status, output

    #创建目标，并返回id
    def create_targets(self,name,hosts):
        cmd = '<create_target><name>{}</name><hosts>{}</hosts></create_target>'.format(name,hosts)
        A.info("Ready to create target.Name:{},hosts:{}".format(name,hosts))
        s,o = self.exec_omp(cmd)
        if s == 0:
            tree = etree.XML(o)
            temp = tree.xpath("/create_target_response/@id")
            target_id = temp[0]
            A.info("Created target Succefful.Target_id:{}".format(target_id))
            return target_id

    """
    def get_targets_id(self,name):
        cmd = '<get_targets/>'
        status,content = self.exec_omp(cmd)
        tree = etree.XML(content)
        tname = tree.xpath("/get_targets_response/target/name")
        tid = tree.xpath("/get_targets_response/target/@id")
        for i in xrange(len(tid)):
            if tname[i].text == name:
                return tid[i]
    """

    def get_configs_id(self,name="Full and fast"):
        cmd = '<get_configs/>'
        A.info("Ready to get config id.Name:{}".format(name))
        status, content = self.exec_omp(cmd)
        tree = etree.XML(content)
        tname = tree.xpath("/get_configs_response/config/name")
        tid = tree.xpath("/get_configs_response/config/@id")
        for i in xrange(len(tid)):
            if tname[i].text == name:
                A.info("Get config id Succefful.Config_id:{}".format(tid[i]))
                return tid[i]

    def get_scanners_id(self,name="OpenVAS Default"):
        cmd = '<get_scanners/>'
        A.info("Ready to get scanner id.Name:{}".format(name))
        status, content = self.exec_omp(cmd)
        tree = etree.XML(content)
        tname = tree.xpath("/get_scanners_response/scanner/name")
        tid = tree.xpath("/get_scanners_response/scanner/@id")
        for i in xrange(len(tid)):
            if tname[i].text == name:
                A.info("Get scanner id Succefful.Config_id:{}".format(tid[i]))
                return tid[i]

    def create_tasks(self,name,config_id,target_id,scanner_id):
        A.info("Ready to create task.Name:{},config_id:{},target_id,scanner_id".format(name,config_id,target_id,scanner_id))
        cmd = '<create_task><name>{}</name><config id="{}"/><target id="{}"/><scanner id="{}"/></create_task>'.format(name,config_id,target_id,scanner_id)
        s,o = self.exec_omp(cmd)
        if s == 0:
            tree = etree.XML(o)
            temp = tree.xpath("/create_task_response/@id")
            task_id = temp[0]
            A.info("Create task successful.Task id:{}".format(task_id))
            return task_id

    def get_tasks_list(self):
        cmd = '<get_tasks/>'
        status, content = self.exec_omp(cmd)
        tree = etree.XML(content)
        tname = tree.xpath("/get_tasks_response/task/name")
        tstatus = tree.xpath("/get_tasks_response/task/status")
        tid = tree.xpath("/get_tasks_response/task/@id")
        trid = tree.xpath("/get_tasks_response/task/last_report/report/@id")
        finish = {}
        running = {}
        j = 0
        for i in xrange(len(tstatus)):
            if tstatus[i].text == "Done":
                finish[tname[i].text] = {'task_id':tid[i],'report_id':trid[j]}
                j+=1
            elif tstatus[i].text == "Running":
                running[tname[i].text] = tid[i]
        dict = {"finish":finish,"running":running}
        return dict

    def get_tasks_id(self,name):
        cmd = '<get_tasks/>'
        status, content = self.exec_omp(cmd)
        tree = etree.XML(content)
        tname = tree.xpath("/get_tasks_response/task/name")
        tid = tree.xpath("/get_tasks_response/task/@id")
        for i in xrange(len(tid)):
            if tname[i].text == name:
                return tid[i]

    def start_task(self,task_id):
        A.info('Start task.Task_id:{}'.format(task_id))
        cmd = '<start_task task_id="{}"/>'.format(task_id)
        s, o = self.exec_omp(cmd)
        return o

    def get_html_report(self,report_id,format_id):
        cmd = '<get_reports report_id="{}" format_id="{}"/>'.format(report_id,format_id)
        s, o = self.exec_omp(cmd)
        tree = etree.XML(o)
        temp = tree.xpath("/get_reports_response/report")
        html = base64.b64decode(temp[0].text)
        return html

    def del_task(self,task_id):
        A.info('Finish Task_id:{},delete it'.format(task_id))
        cmd = '<delete_task task_id="{}"/>'.format(task_id)
        s, o = self.exec_omp(cmd)
        return o

    def get_report_format_id(self,name="HTML"):
        cmd = '<get_report_formats/>'
        status,content = self.exec_omp(cmd)
        tree = etree.XML(content)
        n = tree.xpath("/get_report_formats_response/report_format/name")
        id = tree.xpath("/get_report_formats_response/report_format/@id")
        #print n
        #print id
        for i in xrange(len(n)):
            if n[i].text == name:
                return id[i]

def exec_cmd(cmd):
    status, output = commands.getstatusoutput(cmd)
    return status,output

if __name__=="__main__":
    A = NewLog(print_level='info')
    openvas = OpenVas(user='admin', passwd='1314520')
    while True:
        c = rpyc.connect('192.168.217.1', 7777)
        c.root.set_scan_type('openvas')
        db_running = c.root.get_running()
        result = openvas.get_tasks_list()
        for name,ids in result['finish'].items():
            if name in db_running:
            #获取报告
                format_id = openvas.get_report_format_id()
                #print format_id
                report = openvas.get_html_report(ids['report_id'],format_id)
                with open(name+'_openvas.html','w') as f:
                    f.write(report)
                #更新数据库状态
                db_id = name.split('_')[1]
                c.root.update_status(db_id)
                #删除task
                openvas.del_task(ids['task_id'])
        #当前正在运行任务小于3
        if len(result['running'])<3:
            mission = c.root.get_task()
            if mission:
                target = mission['website']
                name = "task_{}_{}".format(mission['id'], target)
                A.info("Get Task.Target:{},Name:{}".format(target,name))
                target_id = openvas.create_targets(name, target)
                config_id = openvas.get_configs_id()
                scanner_id = openvas.get_scanners_id()
                task_id = openvas.create_tasks(name, config_id=config_id, target_id=target_id, scanner_id=scanner_id)
                openvas.start_task(task_id)
        c.close()
        time.sleep(60)