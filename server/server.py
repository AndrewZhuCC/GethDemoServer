#!/usr/bin/env python
# encoding: utf-8

import os, hashlib
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, jsonify, g, request
import gethbridge as gb

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'geth.db'),
    SECRET_KEY='gethserver',
))

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('users.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database')

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/login', methods=['POST'])
def login():
    user_json = request.get_json(silent=True)
    getcha = False
    userid = None
    try:
        username = user_json['username']
        password = user_json['password']
        db = get_db()
        cur = db.execute('select * from users where uname = ?', [username])
        results = cur.fetchall()
        for result in results:
            if result['pwd'] == password:
                getcha = True
                userid = result['userid']
                break
    except Exception as e:
        print e
        return jsonify(msg='user not found')
    if getcha:
        return jsonify(userid=userid)
    else:
        return jsonify(msg='password error')

@app.route('/register', methods=['POST'])
def register():
    user_json = request.get_json(silent=True)
    userid = None
    try:
        username = user_json['username']
        password = user_json['password']
    except Exception as e:
        print e
        return jsonify(success=False, msg='param error')
    db = get_db()
    cur = db.execute('select * from users where uname = ?', [username])
    results = cur.fetchall()
    if len(results) > 0:
        return jsonify(success=False, msg='already register')
    userid = sha1uname(username)
    db.execute('insert into users (uname, pwd, userid, score) values (?, ?, ?, ?)', [username, password, userid, 0])
    db.commit()
    return jsonify(userid=userid, success=True)

@app.route('/consume', methods=['POST'])
def consume():
    user_json = request.get_json(silent=True)
    try:
        userid = user_json['userid']
        cost = int(user_json['cost'])
    except Exception as e:
        print e
        return jsonify(success=False, msg='param error')
    curScore = 0
    db = get_db()
    cur = db.execute('select * from users where userid = ?', [userid])
    results = cur.fetchall()
    if len(results) == 0:
        return jsonify(success=False, msg='user not found')
    curScore = results[0]['score']
    curScore += (cost / 10)
    db.execute('update users set score = ? where userid = ?', [curScore, userid])
    db.commit()
    gd.addScore(results[0]['id'], (cost / 10))
    return jsonify(success=True, userid=userid)

@app.route('/getScore', methods=['GET'])
def getScore():
    user_json = request.args
    try:
        userid = user_json['userid']
    except Exception as e:
        print e
        return jsonify(msg='param error')
    db = get_db()
    cur = db.execute('select * from users where userid = ?', [userid])
    results = cur.fetchall()
    if len(results) == 0:
        return jsonify(msg='user not found')
    score = results[0]['score']
    return jsonify(userid=userid, score=score)

@app.route('/useScore', methods=['POST'])
def useScore():
    user_json = request.get_json(silent=True)
    try:
        userid = user_json['userid']
        cost = user_json['cost']
    except Exception as e:
        print e
        return jsonify(success=False, msg='param error')
    db = get_db()
    cur = db.execute('select * from users where userid = ?', [userid])
    results = cur.fetchall()
    if len(results) == 0:
        return jsonify(success=False, userid=userid, msg='user not found')
    curscore = results[0]['score']
    if curscore < cost:
        return jsonify(success=False, userid=userid, msg='not enough score')
    curscore -= cost
    db.execute('update users set score = ? where userid = ?', [curscore, userid])
    db.commit()
    gd.useScore(results[0]['id'], cost)
    return jsonify(success=True, userid=userid)

def sha1uname(uname):
    return hashlib.sha1(uname).hexdigest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
