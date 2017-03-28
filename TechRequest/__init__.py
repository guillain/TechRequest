# Target: app init 
# Version: 0.1
# Date: 2017/01/04
# Mail: guillain@gmail.com
# Copyright 2017 GPL - Guillain

from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template, jsonify, flash, send_from_directory
from werkzeug.utils import secure_filename
from static.py.tools import logger, exeReq, wEvent
import re, os, sys, urllib

sys.path.append(os.path.dirname(__file__))

# Conf and create app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTING')

# Import TechRequest features
from static.py.TechRequest import techreq_api
app.register_blueprint(techreq_api)

# WEB mgt ----------------------------------------
@app.route('/')
def my_form():
  if 'login' in session:
    return render_template('new.html')
  return render_template("login.html")

# Login --------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    error = None
    if 'login' in session:
        return render_template('new.html')

    login = request.form['login']
    if not login:
        wEvent('login','','Thanks to provide login','KO')
        return render_template('login.html')

    password = request.form['password']
    if not password:
        wEvent('login','','Thanks to provide password','KO')
        return render_template('login.html')

    try:
        data = exeReq("SELECT uid, grp, email, mobile, admin FROM users WHERE login='"+login+"' AND pw_hash=PASSWORD('"+password+"')")
    except Exception as e:
        wEvent('login','','DB connection/request error', 'KO')
        return render_template('login.html')

    try:
      if data is None or data[0][0] is None:
        wEvent('login','','Wrong email or password','KO')
        return render_template('login.html')
    except Exception as e:
      wEvent('login','','Wrong email or password','KO')
      return render_template('login.html')

    try:
        session['login'] = str(login)
        session['uid'] = str(data[0][0])
        session['grp'] = str(data[0][1])
        session['email'] = str(data[0][2])
        session['mobile'] = str(data[0][3])
        session['admin'] = str(data[0][4])
        wEvent('login',session['uid'],"User "+session['login']+" logged",'OK')
        return render_template('new.html')
    except Exception as e:
        wEvent('login','','Wrong email or password','KO')
        return render_template('login.html')

# Logout --------------------------------------------------
@app.route('/logout')
def logout():
  wEvent('logout',session['uid'],'You were logged out','OK')
  session.clear()
  return redirect('/')

# Server file ---------------------------------------------
@app.route('/uploads/<path:path>')
def send_uploads(path):
    return send_from_directory('uploads', path)

@app.route('/downloads/<path:path>')
def send_downloads(path):
    return send_from_directory('downloads', path)

# Upload file ---------------------------------------------
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        session.pop('filename', None)

        # check if the post request has the file part
        if 'file' not in request.files:
            wEvent('upload_file',session['uid'],'No file part','KO')
            return render_template('upload_file.html', error = 'No file part')
        file = request.files['file']
        if file.filename == '':
            wEvent('upload_file',session['uid'],'No file part','KO')
            return render_template('upload_file.html', error = 'No file part')
        if file and allowed_file(file.filename):
            session['filename'] = str(secure_filename(file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], session['filename']))
            wEvent('upload_file',session['uid'],'File Uploaded, filename: '+session['filename'],'OK')
            return redirect(url_for('uploaded_file', filename=session['filename']))
        else:
            wEvent('upload_file',session['uid'],'File is not allowed','KO')
            return render_template('upload_file.html', error = 'File is not allowed')
    return render_template('upload_file.html')

@app.route('/uploaded_file', methods=['GET', 'POST'])
def uploaded_file():
    wEvent('uploaded_file',session['uid'],'File uploaded for space id','OK')
    return render_template('update.html')


# End of App --------------------------------------------------------------------------
if __name__ == '__main__':
    sess.init_app(app)
    app.debug = True
    app.run()
