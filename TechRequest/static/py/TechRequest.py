# Target: Airlines - Cisco Spark specific integration for Airbus
# Version: 0.1
# Date: 2017/02/05
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template, jsonify, send_file
from werkzeug.utils import secure_filename
from tools import logger, exeReq, wEvent, sEvent, logstash

import urllib2
import json

import re, os, sys, urllib, base64
import pyCiscoSpark

from flask import Blueprint
techreq_api = Blueprint('techreq_api', __name__)

# Conf app
api = Flask(__name__)
api.config.from_object(__name__)
api.config.from_envvar('FLASK_SETTING')

# Dashboard ---------------------------------------
@techreq_api.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    error = None
    if request.method == 'POST':
        # Set timer session value cming from the web
        session['timer'] = request.form['timer'];
        print 'timer: ' + session['timer']

        # Get data according to the admin priv
        if session['admin'] == '1':
            sql  = "SELECT 'admin', s.sid, s.name, 'list', DATE_FORMAT(s.birthday, '%Y-%m-%d'), "
            sql += "DATE_FORMAT(s.timestamp, '%Y-%m-%d %H:%i'), s.severity, s.status "
            sql += "FROM spaces s, users u WHERE u.uid = s.uid AND u.uid != '1' AND s.status NOT LIKE '%close%' GROUP BY s.name ORDER BY s.name;"
        else:
            sql  = "SELECT '"+session['grp']+"', s.sid, s.name, 'Me', "
            sql += "DATE_FORMAT(s.birthday, '%Y-%m-%d'), DATE_FORMAT(s.timestamp, '%Y-%m-%d %H:%i'), s.severity, s.status "
            sql += "FROM spaces s WHERE s.uid = '"+session['uid']+"' AND u.uid != '1' AND s.status NOT LIKE '%close%' ORDER BY s.name;" 
        try:
            spaces = exeReq(sql)
        except Exception as e:
            wEvent('dashboard',session['uid'],'Database error (get dashboard data)','KO')
            return render_template('index.html')
        return jsonify(data=spaces)
    else:
      return 'Dashboard refreshed'

# New -------------------------------------------
@techreq_api.route('/new', methods=['POST', 'GET'])
def new():
    session.pop('filename', None)
    return render_template('new.html')

@techreq_api.route('/newSub', methods=['POST'])
def newSub():
    error = None

    # Get POST param
    title = str(request.form['title'])
    if not title:
        wEvent('newSub',session['uid'],'Thanks to provide title','KO')
        return 'Thanks to provide title'

    description = str(request.form['description'])
    if not description:
        wEvent('newSub',session['uid'],'Thanks to provide description','KO')
        return 'Thanks to provide description'

    severity = str(request.form['severity'])
    if not severity:
        wEvent('newSub',session['uid'],'Thanks to provide severity','KO')
        return 'Thanks to provide severity'

    # Create Space
    try:
        space = pyCiscoSpark.post_room(api.config['ACCESS_TOKEN'],title)
        session['sid'] = space['id']
        session['sname'] = title
        sEvent('creation')
        wEvent('newSub',session['uid'],"Space created, id: "+space['id'],'OK')
    except Exception as e:
        wEvent('newSub',session['uid'],"Issue during space creation, name: "+title,'KO')
        return "Issue during space creation"

    # Create webhook
    try:
        webhookmsg = pyCiscoSpark.post_webhook(api.config['ACCESS_TOKEN'], title, api.config['SPARK_WEBHOOK']+'/message', 'messages', 'all', str('roomId='+space['id']))
        exeReq("INSERT INTO spaces VALUES ('"+space['id']+"','1','"+webhookmsg['id']+"','open', '', CURDATE(), NOW());")
        wEvent('newSub',session['uid'],"Webhook created, space id: "+space['id'],'OK')
    except Exception as e:
        wEvent('newSub',session['uid'],"Issue during webhook space creation, name: "+title,'KO')
        return "Issue during webhook space creation"

    # Get members from DB and associat to the Space (remote+local)
    try:
        member_list = exeReq("SELECT DISTINCT email,uid,login,admin FROM users WHERE grp = 'EXP' OR grp = 'FR' OR grp = 'AL';")
    except Exception as e:
        wEvent('newSub',session['uid'],'Database error (get member_list data)','KO')
        return 'Database error (get member_list data)'
    for user in member_list:
        try:
            pyCiscoSpark.post_roommembership(api.config['ACCESS_TOKEN'],space['id'],user[0],user[3])
            exeReq("INSERT INTO spaces VALUES ('"+space['id']+"','"+str(user[1])+"','"+title+"','open', '"+severity+"', CURDATE(), NOW());")
            sEvent('Membership added:'+user[0])
            wEvent('newSub',session['uid'],"User "+user[0]+" add to the space "+title,'OK')
        except Exception as e:
            wEvent('newSub',session['uid'],"Issue when add user "+user[0]+" to the space "+title,'KO')

    # Post TechRequest initial messages in the Space
    msg = 'Welcome in the new TechRequest Space'
    msg += '\n- Title: ' + title
    msg += '\n- Description: ' + description
    msg += '\n- Severity: ' + severity
    msg += '\n- Requestor: ' + session['login']
    msg += '\n- Requestor email: ' + session['email']
    msg += '\n- Webserver: ' + api.config['SPARK_WEBHOOK']
    msg += '\n- Space ID: ' + session['sid']
    msg += '\nRemember that you can use the following bot in 1:1 space for additionnal support'
    msg += '\n- TechRequest.io : specific support for TechRequest'
    msg += '\n- SparkBotAdv@sparkbot.io : additionnal tool like translator, crisis room, search engine'
    msg_dict = pyCiscoSpark.post_message(api.config['ACCESS_TOKEN'],space['id'],msg)
    sEvent('Initial messages recorded:\n\n'+msg)
    wEvent('newSub',session['uid'],'Messages put in the space','OK')

    # End of first inital TechRequest
    session['filename'] = ''
    return 'Space created and people invited'

# Update ----------------------------------------
@techreq_api.route('/update', methods=['POST', 'GET'])
def update():
    session['sname'] = request.form['sname']
    session['sid'] = request.form['sid']
    return render_template('update.html')

@techreq_api.route('/updateSub', methods=['POST'])
def updateSub():
    error = None

    # Get param
    description = str(request.form['description'])
    if not description:
        wEvent('updateSub',session['uid'],'Thanks to provide description','KO')
        return 'Thanks to provide description'

    msg = 'TechRequest udpate from '+session['grp']
    msg += '\n- Description: ' + description

    try:
        severity = str(request.form['severity'])
        if severity:
            msg += '\n- Severity: ' + severity
            try:
                exeReq("UPDATE spaces SET severity = '"+severity+"' WHERE sid = '"+session['sid']+"';")
            except Exception as e:
                wEvent('updateSub',session['uid'],'Issue during severity update in local DB','KO')
    except Exception as e:
        wEvent('updateSub',session['uid'],'Issue during severity treatment','OK')

    fileurl = 'no file provided'
    if 'filename' in session:
        if session['filename']:
            wEvent('updateSub',session['uid'],'File provided: '+session['filename'],'OK')
            fileurl = api.config['UPLOAD_URL']+session['filename']
            fileurlspark = api.config['UPLOAD_URL_SPARK']+session['filename']
            msg += '\n- File: ' + fileurl
        else:
            wEvent('updateSub',session['uid'],'No filename provided','KO')
    else:
        wEvent('updateSub',session['uid'],'No file provided','KO')

    # Post file in the Space
    if fileurl != 'no file provided':
        try:
            file_dict = pyCiscoSpark.post_file(api.config['ACCESS_TOKEN'],session['sid'], fileurlspark)
            wEvent('updateSub',session['uid'],"File "+session['filename']+" posted to the space "+session['sid'],'KO')
        except Exception as e:
            wEvent('updateSub',session['uid'],"Issue when post file url "+fileurl+" to the space "+session['sid'],'KO')

    # Post TechRequest update messages in the Space
    session['filename'] = ''
    try:
        msg_dict = pyCiscoSpark.post_message(api.config['ACCESS_TOKEN'],session['sid'],msg)
        return 'Update done'
    except Exception as e:
        wEvent('updateSub',session['uid'],"Issue during message update",'KO')
        return render_template('update.html')


# Bot messages ----------------------------------------------------------
@techreq_api.route('/message', methods=['POST'])
def message():
    print 'message received'
    jso = json.loads(request.data)
    data = jso.get('data')

    try:
        msg = pyCiscoSpark.get_message(api.config['ACCESS_TOKEN'],data.get('id'))
    except Exception as e:
        wEvent('message','webhook','Get Spark message error','KO')
        return 'Get Spark message error'

    try:
        exeReq("INSERT INTO sEvents SET sid = '"+data.get('roomId')+"', msg = '"+msg.get('text')+"', uid = '0';")
        logstash('bot',msg)
        wEvent('message','webhook','Messages stored locally','OK')
        return 'Message stored locally'
    except Exception as e:
        wEvent('message','webhook','Database error (put msg data)','KO')
        return 'Database error (put msg data)'

# User ------------------------------------------
@techreq_api.route('/user', methods=['POST', 'GET'])
def user():
    try:
        user = exeReq("SELECT login,email,mobile,admin,grp FROM users WHERE login = '"+request.args['login']+"';")
        return render_template('user.html', user = user[0])
    except Exception as e:
        wEvent('user','webhook','Get user error','KO')
        return 'Get user error'

@techreq_api.route('/userupdate', methods=['POST','GET'])
def userSub():
    try:
        sql  = "UPDATE users SET "
        sql += "  email = '"+request.form['email']+"', "
        sql += "  admin = '"+request.form['admin']+"', "
        sql += "  grp = '"+request.form['group']+"', "
        sql += "  mobile = '"+request.form['mobil']+"' "
        sql += "WHERE login = '"+request.form['login']+"';"
    except Exception as e:
        wEvent('user','webhook','SQL request preparation issue','KO')
        return 'SQL request preparation issue'

    try:
        user = exeReq(sql)
        wEvent('user','webhook','User update OK','OK')
        return 'User update OK'
    except Exception as e:
        wEvent('user','webhook','User update error','KO')
        return 'User update error'

# Users ------------------------------------------
@techreq_api.route('/users', methods=['POST', 'GET'])
def users():
    try:
        users = exeReq("SELECT login,email,admin,grp FROM users WHERE uid != '1';")
        return render_template('users.html', users = users)
    except Exception as e:
        wEvent('users','webhook','Get user list error','KO')
        return 'Get user list error'

@techreq_api.route('/usersSub', methods=['POST'])
def usersSub():
    error = None
    return 'OK'

# View ------------------------------------------------------------------
@techreq_api.route('/view', methods=['POST'])
def view():
  if not request.form['sid']:
    wEvent('view',session['uid'],"No space ID provided",'KO')
    return 'No space ID provided'

  session['sname'] = request.form['sname']
  session['sid'] = request.form['sid']
  try:
    msg_dict = pyCiscoSpark.get_messages(api.config['ACCESS_TOKEN'],session['sid'])
    sEvent('view')
    wEvent('view',session['uid'],"Space viewed, id: "+session['sid'],'OK')
    return render_template('view.html', data=msg_dict)
  except Exception as e:
    wEvent('view',session['uid'],str("Issue to list the messages, id "+session['sid']),'KO')
    return 'Issue during space message listing'

# Close ------------------------------------------------------------------
@techreq_api.route('/close', methods=['POST'])
def close():
  if not request.form['sid']:
    wEvent('close',session['uid'],"No space ID provided",'KO')
    return 'No space ID provided'

  session['sname'] = request.form['sname']
  session['sid'] = request.form['sid']
  try:
    # Delete webhook
    webhook = exeReq("SELECT name FROM spaces WHERE uid = '1' AND sid = '" + session['sid'] + "';")
    web = pyCiscoSpark.del_webhook(api.config['ACCESS_TOKEN'],webhook[0][0])

    # Delete room
    pyCiscoSpark.del_room(api.config['ACCESS_TOKEN'],session['sid'])
    exeReq("UPDATE spaces SET status = 'close' WHERE sid = '"+session['sid']+"';")

    # Log
    sEvent('closure')
    wEvent('close',session['uid'],"Space closed, id: "+session['sid'],'OK')
    return render_template('new.html')
  except Exception as e:
    wEvent('close',session['uid'],str("Issue to close the space, id "+session['sid']),'KO')
    return 'Issue during space closure'

# Dump -------------------------------------------------------------------
@techreq_api.route('/dump', methods=['POST'])
def dump():
  if not request.form['sid']:
    wEvent('dump',session['uid'],"No space ID provided",'KO')
    return 'No space ID provided'

  session['sname'] = request.form['sname']
  session['sid'] = request.form['sid']

  # Dump the Space
  try:
    msg_dict = pyCiscoSpark.get_messages(api.config['ACCESS_TOKEN'],session['sid']) 
    sEvent('dump')
  except Exception as e:
    wEvent('dump',session['uid'],"Issue to dump the space "+session['sid'],'KO')

  # Get file from message
  try:
    for msg in msg_dict['items']:
      if 'files' in msg:
        fileurl = str(msg['files'])
        fileurl = fileurl.replace("[u'https://api.ciscospark.com/v1/contents/", "")
        fileurl = fileurl.replace("']","")

        response = pyCiscoSpark.get_content(api.config['ACCESS_TOKEN'],fileurl)
        content_disp = response.headers.get('Content-Disposition', None)

        if content_disp is not None:
          filename = content_disp.split("filename=")[1]
          filename = filename.replace('"', '')
          with open(filename, 'w') as f:
            f.write(response.read())
            print 'Saved-', filename
        else:
          print "Cannot save file- no Content-Disposition header received."

  except Exception as e:
    wEvent('dump',session['uid'],"Issue to get file in message "+session['sid'],'KO')

  # Dump the database
  try:
    database = exeReq("Select * FROM spaces s, sEvents e WHERE s.sid = '"+session['sid']+"' AND e.sid = '"+session['sid']+"';")
  except Exception as e:
    wEvent('dump',session['uid'],"Issue to dump the database "+session['sid'],'KO')

  # Write data into single CSV file
  msg = 'TechRequest Dump generation for the Space:'+session['sid']
  msg += '\n\nSpace dump\n'+str(msg_dict)
  msg += '\n\nDatabase dump\n'+str(database)

  try:
    with open(api.config['DOWNLOAD_FOLDER']+session['sid']+".csv","wb") as fo:
      fo.write(msg)
  except Exception as e:
    wEvent('dump',session['uid'],str("Issue to create the file "+session['sid']),'KO')

  wEvent('dump',session['uid'],"Space dumped, id: "+session['sid'],'OK')
  return send_file(api.config['DOWNLOAD_FOLDER']+session['sid']+".csv")

