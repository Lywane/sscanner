import rpyc

c = rpyc.connect('192.168.217.130', 8888)
#c.root.set_scan_type('openvas')

#print c.root.get_running()
#print c.root.get_task()
#print c.root.update_status(1)
print c.root.get_openvas_html(1)
c.close()
