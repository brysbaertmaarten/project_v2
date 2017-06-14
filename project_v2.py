from flask import Flask, Response, request, redirect, url_for, session, flash
from flask import render_template

import Servomotor, Led, Buzzer, camera, DbClass, motion_sensor

from sys import executable
from subprocess import Popen

import time, os, datetime
app = Flask(__name__)

#start motion detection
motion_sensor.MotionSensor()

@app.before_request
def before_request():
    print(request.path)
    if request.path != '/login' or request.path == '/logout':
        if not session.get('logged_in'):
           return render_template('login.html')

#HOME
process = None #initialiseren
@app.route('/')
def home():
    global process
    if process != None:
        process.terminate() #als er nog een process bezig is, stop het
    process = Popen([executable, '/home/pi/Documents/python/project_v2/static/pistreaming/server.py'])  # start stream
    time.sleep(2)
    return render_template('home.html')


@app.route('/login', methods=['POST'])
def login():
    accountgegevens = DbClass.DbClass().getDataFromDatabase('account')[0]
    if request.form['password'] == accountgegevens[5] and request.form['username'] == accountgegevens[1]:
        session['logged_in'] = True
    else:
        flash('wrong password')
    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('login.html')


@app.route('/start_recording', methods=['POST'])
def start_recording():
    process.terminate()
    time.sleep(1)
    name = request.form['name']
    dateTime = datetime.datetime.now()
    DbClass.DbClass().insertMedia(0, name, 1, dateTime)
    data = DbClass.DbClass().getDataFromDatabaseMetVoorwaarde('media', 'date', dateTime)
    identifier = data[0][0]
    camera.PiCam().start_record(str(identifier))
    return redirect('/')


@app.route('/capture', methods=['POST'])
def capture():
    process.terminate()
    time.sleep(1)
    name = request.form['name']
    dateTime = datetime.datetime.now()
    DbClass.DbClass().insertMedia(0, name, 0, dateTime)
    data = DbClass.DbClass().getDataFromDatabaseMetVoorwaarde('media', 'date', dateTime)
    identifier = data[0][0]
    camera.PiCam().capture(str(identifier))
    return redirect('/')


@app.route('/rotate', methods=['POST'])
def rotate():
    position = DbClass.DbClass().getDataFromDatabase('settings')[0][2]
    richting = request.form['richting']
    if richting == "l":
        Servomotor.ServoMotor(19, position).step_left()
        new_position = position + 10
        if new_position > 100 or new_position < 0:
            new_position = position
        DbClass.DbClass().updateData('settings', 'pan', new_position)

    elif richting == "r":
        Servomotor.ServoMotor(19, position).step_right()
        new_position = position - 10
        if new_position > 100 or new_position < 0:
            new_position = position
        DbClass.DbClass().updateData('settings', 'pan', new_position)
    return 'rotate'


@app.route('/led')
def led():
    Led.LedLamp(26).flikker_bg(5)
    return redirect('/')


@app.route('/buzzer')
def buzzer():
    Buzzer.Buzzer(13).alarm_bg(5)
    return redirect('/')


@app.route('/account')
def account():
    accountgegevens = DbClass.DbClass().getDataFromDatabase('account')
    return render_template("account.html", accountgegevens=accountgegevens, updated=False)


@app.route('/account/update', methods=['POST'])
def account_update():
    result = request.form
    DbClass.DbClass().updateData('account', 'username', result["username"])
    DbClass.DbClass().updateData('account', 'first_name', result["first_name"])
    DbClass.DbClass().updateData('account', 'last_name', result["last_name"])
    DbClass.DbClass().updateData('account', 'email', result["email"])
    DbClass.DbClass().updateData('account', 'password', result["password"])

    accountgegevens = DbClass.DbClass().getDataFromDatabase('account')

    return render_template("account.html", accountgegevens=accountgegevens, updated=True)


@app.route('/securitymode')
def securitymode():
    settings = DbClass.DbClass().getDataFromDatabase('settings')
    return render_template('securitymode.html', settings=settings, updated=False)

@app.route('/securitymode/update', methods=['POST'])
def securitymode_update():
    result = request.form
    def get_bool(key):
        try:
            if result[key]:
                return 1
        except:
            return 0
    DbClass.DbClass().updateData('settings', 'securitymode', get_bool("securitymode"))
    DbClass.DbClass().updateData('settings', 'alarm', get_bool("alarm"))
    DbClass.DbClass().updateData('settings', 'led', get_bool("led"))
    DbClass.DbClass().updateData('settings', 'email', get_bool("email"))
    settings = DbClass.DbClass().getDataFromDatabase('settings')
    return render_template('securitymode.html', settings=settings, updated=True)


@app.route('/capturedmedia')
def captured_media():
    return render_template('captured-media.html')

@app.route('/get_media', methods=['POST'])
def get_media():
    result = request.form
    data = DbClass.DbClass().getMedia(result['type'], 0, result['naam'], result["date"])
    return render_template('captured-media.html', data=data)


@app.route('/delete/<id>/<extensie>')
def delete(id, extensie):
    delete = True
    print(id)
    print(extensie)
    try:
        DbClass.DbClass().delete_media(id)
        os.system('rm /home/pi/Documents/python/project_v2/static/media/' + id + extensie)
    except:
        delete = False
    return render_template('captured-media.html', delete=delete)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", debug=True)