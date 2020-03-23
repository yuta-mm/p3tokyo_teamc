import io
import csv
import pprint
from flask import Flask, render_template, request, jsonify
from wtforms import Form, StringField, SubmitField, validators, ValidationError
import numpy as np
from sklearn.externals import joblib
from flask_table import Table, Col    

app = Flask(__name__)

class Item(object):
    def __init__(self, name, description1):
        self.name = name
        self.description1 = description1
        

class LogItem(object):
    def __init__(self, name, description1, description2):
        self.name = name
        self.description1 = description1
        self.description2 = description2


class ItemTable(Table):
    name = Col('名前')
    description1 = Col('出席時刻')
    

class LogItemTable(Table):
    name = Col('名前')
    description1 = Col('時刻')
    description1 = Col('入退状況')


class addUser(Form):
    username = StringField("登録者の名前",
                           [validators.InputRequired("この項目は入力必須です")])

    # html側で表示するsubmitボタンの表示
    submit = SubmitField("追加")

memberlist = []
attendance = {}
attendTime = {}
exitTime = {}
logdictlist = []

def update_dict(logdictlist):
    d_len = len(logdictlist)

    for i in range(d_len):
        if logdictlist[i]['state'] == 'in':
            attendance[logdictlist[i]['name']] = True
            attendTime[logdictlist[i]['name']] = logdictlist[i]['time']

        if logdictlist[i]['state'] == 'out':
            attendance[logdictlist[i]['name']] = False
            exitTime[logdictlist[i]['name']] = logdictlist[i]['time']


@app.route('/')
def index1():
    return render_template('index1.html')

@app.route('/conf/')
def index2():
    items = []
    length = len(memberlist)
    
    if length == 0:
        return render_template('index2_n.html')

    with open('face_log.csv') as f:
        reader = csv.DictReader(f)
        logdictlist = [row for row in reader]

    loglength = len(logdictlist)
    print(loglength)

    update_dict(logdictlist)

    for i in range(length):
        name = memberlist[i]
        if attendance[name]:
            items.append(Item(name, attendTime[name]))
            
    table = ItemTable(items)
    return render_template('index2.html', table=table)

@app.route('/log/')
def index2_log():
    logitems = []

    with open('face_log.csv') as f:
        reader = csv.DictReader(f)
        logdictlist = [row for row in reader]

    loglength = len(logdictlist)
    print(loglength)

    for i in range(loglength):
        logitems.append(LogItem(logdictlist[i]['name'], logdictlist[i]['time'], logdictlist[i]['state']))

    logtable = LogItemTable(logitems)
    return render_template('index2_log.html', logtable=logtable)

@app.route('/create/', methods = ['GET', 'POST'])
def index3():
    form = addUser(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('index3.html', form=form)
        else:
            memberlist.append(request.form["username"])
            attendance[request.form["username"]]=False
            attendTime[request.form["username"]]='-'
            exitTime[request.form["username"]]='-'

            print(memberlist)

            return render_template('index3.html', form=form)
    elif request.method == 'GET':
        
        return render_template('index3.html', form=form)

@app.route('/camera/')
def index4():
    return render_template('index4.html')

@app.route('/init/')
def index5():
    memberlist.clear()
    attendance.clear()
    attendTime.clear()
    exitTime.clear()
    return render_template('index5.html')

if __name__ == "__main__":
    app.run(port=8000, debug=True)

