# -*- coding: utf-8 -*-

import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import rpyc
import requests
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from NewLog import NewLog



class Nessus():
    
    def __init__(self,ip,port,accesskey,secretkey):
        self.ip = ip
        self.port = port
        self.accesskey = accesskey
        self.secretkey = secretkey
        self.header = {
            'X-ApiKeys': 'accessKey={};secretKey={}'.format(accesskey, secretkey),
            'Content-type': 'application/json',
            'Accept': 'text/plain'
        }

    def get_folder_id(self,folder_name="My Scans"):
        # 返回结果
        result = ''
        # 调用/folders接口
        url = "https://{}:{}/scans".format(self.ip,self.port)
        respon = requests.get(url, headers=self.header, verify=False)
        # 请求成功，则返回结果，否则返回空值
        if respon.status_code == 200:
            result = json.loads(respon.text)
            for i in result.get('folders'):
                if i.get('name') == folder_name:
                    result = i.get('id')
        return result

    def get_uuid(self):
        # 返回结果
        result = ''
        # 调用/folders接口
        url = "https://{}:{}/editor/scan/templates".format(self.ip,self.port)

        respon = requests.get(url, headers=self.header, verify=False)
        # 请求成功，则返回结果，否则返回空值
        if respon.status_code == 200:
            result = json.loads(respon.text)
            for i in result.get('templates'):
                if i.get('title') == "Web Application Tests":
                    result = i.get('uuid')
        return result

    def create_scan(self,name, target):
        uuid = self.get_uuid()
        folder_id = self.get_folder_id()
        url = "https://{}:{}/scans".format(self.ip,self.port)
        data = {"uuid": uuid,
                "settings": {"name": name, "enabled": "false", "launch_now": "true", "folder_id": folder_id,
                             "text_targets": target}}
        respon = requests.post(url, data=json.dumps(data), headers=self.header, verify=False)
        if respon.status_code == 200:
            return json.loads(respon.text)

    def get_detail(self,scan_id):
        # 返回结果
        result = ''
        # 调用/folders接口
        url = "https://{}:{}/scans/{}".format(self.ip,self.port,scan_id)

        respon = requests.get(url, headers=self.header, verify=False)
        # 请求成功，则返回结果，否则返回空值
        if respon.status_code == 200:
            result = json.loads(respon.text)
        return result

    def get_scan_list(self):
        # 返回结果
        res = {"running": [], "completed": []}
        # 调用/folders接口
        url = "https://{}:{}/scans".format(self.ip,self.port)

        respon = requests.get(url, headers=self.header, verify=False)
        # 请求成功，则返回结果，否则返回空值
        if respon.status_code == 200:
            result = json.loads(respon.text)
            if result.get('scans'):
                for i in result.get('folders'):
                    if i["name"] == "My Scans":
                        id = i["id"]
                        break
                for j in result.get('scans'):
                    if j["folder_id"] == id:
                        if j["status"] == 'running':
                            res['running'].append(j)
                        elif j["status"] == 'completed':
                            #if int(time.time()) - int(j['last_modification_date']) < 600:
                            res['completed'].append(j)
        A.info("This is scan list:{}".format(res))
        return res

    def move_to_trash(self,scan_id):
        A.info("The scan_id {} finish.Delete it".format(scan_id))
        trash_id = self.get_folder_id('Trash')
        url = "https://{}:{}/scans/{}/folder".format(self.ip, self.port, scan_id)
        data = {'folder_id': trash_id}
        r = requests.put(url, data=json.dumps(data),headers=self.header, verify=False)
        return True if r.status_code == 200 else False


    def del_scan(self,scan_id):
        url = "https://{}:{}/scans/{}".format(self.ip,self.port,scan_id)
        r = requests.delete(url, headers=self.header, verify=False)
        return True if r.status_code == 200 else False

    def get_html(self,scan_id, filename):
        A.info("The {} finish".format(filename))
        url = "https://{}:{}/scans/{}/export".format(self.ip,self.port,scan_id)
        data_summary = {'format': "html", 'chapters': "vuln_hosts_summary"}
        data_detail = {'format': "html", 'chapters': "vuln_by_host"}
        summary = requests.post(url, headers=self.header, data=json.dumps(data_summary), verify=False)

        if summary.status_code == 200:
            result = json.loads(summary.text)
            url_token = "https://{}:{}/tokens/{}/download".format(self.ip,self.port,result['token'])
            time.sleep(1)
            res = requests.get(url_token, headers=self.header, verify=False)
            if res.status_code == 200:
                with open("{}_summary.html".format(filename), 'w') as f:
                    f.write(res.text)
        detail = requests.post(url, headers=self.header, data=json.dumps(data_detail), verify=False)
        if detail.status_code == 200:
            result = json.loads(detail.text)
            url_token = "https://{}:{}/tokens/{}/download".format(self.ip,self.port,result['token'])
            time.sleep(1)
            res = requests.get(url_token, headers=self.header, verify=False)
            if res.status_code == 200:
                with open("{}_detail.html".format(filename), 'w') as f:
                    f.write(res.text)


if __name__=="__main__":
    # Nessus生成的API key
    A = NewLog(print_level='info')
    accesskey = '67fe24b355185e7a973c41538f6d38748395291b50b4c324cd215a2a0846b6b8'
    secretkey = '75977aeb6c3f31b61690390c9d69ec22c60209eeaafd7faae1e4684a1f990c47'
    # 组装请求
    r = "task_(\d+)_(.+)"
    nessus = Nessus('192.168.217.128',8834,accesskey,secretkey)
    while True:
        status = nessus.get_scan_list()
        c = rpyc.connect('127.0.0.1', 7777)
        #先查有没有完成的
        c.root.set_scan_type('nessus')
        db_running = c.root.get_running()

        for scan in status['completed']:
            if db_running:
                if scan['name'] in db_running:
                    #获取报告 get_detail(scan_id)
                    nessus.get_html(scan['id'],scan['name'])
                    id = re.match(r,scan['name']).group(1)
                    print "{} has finish".format(scan['name'])
                    c.root.update_status(id)
                    nessus.move_to_trash(scan['id'])
                    #nessus.del_scan(scan['id'])
                #get_detail()
        #查当前任务数量，不到3就拿过来新的
        if len(status['running'])<2:
            mission = c.root.get_task()
            if mission:
                target = mission['website']
                name = "task_{}_{}".format(mission['id'], target)
                print "{} ready to start".format(name)
                nessus.create_scan(name, target)
        c.close()
        time.sleep(60)
