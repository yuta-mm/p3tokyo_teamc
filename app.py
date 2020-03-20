from flask import Flask, render_template, request
from wtforms import Form, StringField, SubmitField, validators, ValidationError
import numpy as np
from sklearn.externals import joblib
from flask_table import Table, Col

app = Flask(__name__)

class Item(object):
    def __init__(self, name, description1, description2, description3):
        self.name = name
        self.description1 = description1
        self.description2 = description2
        self.description3 = description3


class ItemTable(Table):
    name = Col('名前')
    description1 = Col('出欠状況')
    description2 = Col('出席時刻')
    description3 = Col('退出時刻')


class addUser(Form):
    username = StringField("登録者の名前",
                           [validators.InputRequired("この項目は入力必須です")])

    # html側で表示するsubmitボタンの表示
    submit = SubmitField("追加")

memberlist = []
attendance = {}
attendTime = {}
exitTime = {}

@app.route('/')
def index1():
    return render_template('index1.html')

@app.route('/conf/')
def index2():
    items = []
    length = len(memberlist)

    if length == 0:
        return render_template('index2_n.html')

    for i in range(length):
        name = memberlist[i]
        items.append(Item(name, attendance[name], attendTime[name], exitTime[name]))
            
    table = ItemTable(items)
    return render_template('index2.html', table=table)

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

