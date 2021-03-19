# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 14:18:44 2020

@author: ljh
"""

from flask import Flask,request,render_template
from flask_cors import CORS
import sqlite3
import json
#连接SQLite数据库

port = [5000]
app = Flask(__name__)
CORS(app, resources=r'/*')


#创建表
conn = sqlite3.connect('agent.db',isolation_level=None,check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE if not exists agent(
    id int primary key,
    name char(16),
    x int DEFAULT 0,
    y int DEFAULT 0,
    state short DEFAULT 0,
    crtdate timestamp default (datetime('now','localtime')),
    upddate timestamp default (datetime('now','localtime'))
    )''')
conn.close()

@app.route('/GET/data',methods=['get','post'])
def get_list():
    list = []
    conn = sqlite3.connect('agent.db',isolation_level=None,check_same_thread=False)
    c = conn.cursor()
    cursor = c.execute('''SELECT id,name,x,y,state from agent''')
    res = c.fetchall()
    for row in res:
        dict={'id':row[0],
            'name':row[1],
            'x':row[2],
            'y':row[3],
            'state':row[4]}
        list.append(dict)
    conn.close()
    return json.dumps(list)

@app.route('/POST/item',methods=['get','post'])
def add_list():
    data = request.get_data()
    data = json.loads(data)
    conn = sqlite3.connect('agent.db',isolation_level=None,check_same_thread=False)
    c = conn.cursor()
    c.execute('''INSERT INTO agent(id,name,x,y,state)\
          VALUES (?,?,?,?,?)''',(data['id'],data['name'],data['x'],data['y'],data['state']))
    conn.close()
    return json.dumps(
        {'status' : 0})

@app.route('/DELETE/<id>',methods=['get','post'])
def del_list(id):
    conn = sqlite3.connect('agent.db',isolation_level=None,check_same_thread=False)
    c = conn.cursor()
    c.execute('''DELETE from agent where id=?;''',id)
    conn.close()
    return json.dumps(
        {'status' : 0})

@app.route('/PUT/item',methods=['get','post'])
def change_list():
    data = request.get_data()
    data = json.loads(data)
    conn = sqlite3.connect('agent.db',isolation_level=None,check_same_thread=False)
    c = conn.cursor()
    if data['form'] == 'name':
        c.execute('''UPDATE agent set name = ? where id=?''',(data['value'],data['id']))
    if data['form'] == 'x':
        c.execute('''UPDATE agent set x = ? where id=?''',(data['value'],data['id']))
    if data['form'] == 'y':
        c.execute('''UPDATE agent set y = ? where id=?''',(data['value'],data['id']))
    if data['form'] == 'state':
        c.execute('''UPDATE agent set state = ? where id=?''',(data['value'],data['id']))
    conn.close()
    return json.dumps(
        {'status' : 0})
    

if __name__ == '__main__':
    app.run()