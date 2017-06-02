# Target: tools for the app (db, wEvent, logger)
# Version: 0.1
# Date: 2017/01/18
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, flash, session
import MySQLdb

# Import settings
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# Log functions -----------------------
# Log function (push in flash + log)
def logger(fct,msg):
  flash(msg)
  print(str(fct+": "+msg))
  return

# Event recorded 
def wEvent(module, user, msg, status = None):
  logger(module,msg)
  logstash('syslog', {'module:' + module + ',user:' + user + ",msg:" + msg})
  return exeReq("INSERT INTO events (module, user, msg, status) VALUES ('"+module+"', '"+user+"', '"+msg+"', '"+status+"');")

# Space log in DB
def sEvent(msg):
  return exeReq("INSERT INTO sEvents (sid,uid,msg) VALUES ('"+session['sid']+"', '"+session['uid']+"', '"+msg+"');")

# Logstash connector for bot and syslog

# Create Analytics connector if analytics feature is activated
if( app.config['ANALYTICS'] == 'true'):
  import logging, sys, logstash, datetime, jsonify

  analytics = logging.getLogger('python-logstash-logger')
  analytics.setLevel(logging.INFO)
  analytics.addHandler(logstash.TCPLogstashHandler(
    app.config['ANALYTICS_HOST'],
    app.config['ANALYTICS_PORT'],
    version=app.config['ANALYTICS_VERSION']))

def logstash(type,data):
  # If Analytics feaure activated
  if( app.config['ANALYTICS'] == 'true'):
    print 'Analytics data push'

    # Logstash for bot message
    if ( type == 'bot' ):
      print 'Type: bot'
      analytics.info(data, extra={'type': 'bot'})

    # Logstash for syslog
    else:
      print 'Type: syslog'
      analytics.info(str(data), extra={'type': 'syslog'})

# MySQL functions ---------------------
# MySQL connector
def connection():
    conn = MySQLdb.connect(
        host = app.config['MYSQL_HOST'],
        user = app.config['MYSQL_USER'],
        passwd = app.config['MYSQL_PASSWORD'],
        db = app.config['MYSQL_DB']
    )
    c = conn.cursor()
    return c, conn


def exeReq(req):
    error = None

    try:
        c, conn = connection()
    except Exception as e:
        logger('DB connection issue')
        return e

    try:
        c.execute(req)
        conn.commit()
    except Exception as e:
        logger('DB req execution issue')
        return e

    try:
        d = c.fetchall()
        c.close()
        return d
    except Exception as e:
        logger('DB fetch data issue')
        return e


