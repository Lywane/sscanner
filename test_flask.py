import re
import rpyc
from flask import Flask,render_template,request
app = Flask(__name__)

@app.route('/add_task', methods=['GET', 'POST'])
def add_tesk():
    name = request.form.get('Name')
    website = request.form.get('WebSite')
    scan = None
    error = {'error'}
    if isip(website) or isdomain(website):
        c = rpyc.connect('127.0.0.1', 7777)
        scan = c.root.insert(name, website)
        c.close()
    return scan if scan else error


@app.route('/')
def hello_world():
    return render_template('te.html')

@app.route('/check_task/<u>')
def show(u):
    temp = u.split('_')
    if len(temp)==3:
        id = temp[1]
        website = temp[2]
        c = rpyc.connect('127.0.0.1', 7777)
        result = c.root.check_status(id,website)
        c.close()
        return result

@app.route('/check_task/detail/<u>')
def detail(u):
    c = rpyc.connect('127.0.0.1', 8888)
    result = c.root.get_detail_html(u)
    c.close()
    return result

@app.route('/check_task/summary/<u>')
def summary(u):
    c = rpyc.connect('127.0.0.1', 8888)
    result = c.root.get_summary_html(u)
    c.close()
    return result

@app.route('/check_task/openvas/<u>')
def openvas(u):
    c = rpyc.connect('127.0.0.1', 8888)
    result = c.root.get_summary_html(u)
    c.close()
    return result

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post ' + str(post_id)

def isdomain(string):
    return True


def isip(string):
    r = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    ip = re.search(r,'string')
    return False if ip == None else True


if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True)

