from flask import Flask, Response, request, redirect, url_for
from flask import render_template
import os
import Servomotor
import Led
import DbClass
import datetime
import camera
app = Flask(__name__)

#test
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start_recording')
def start_recording():
    dateTime = datetime.datetime.now()
    DbClass.DbClass().setDataToDatabase("media","date",dateTime)

    data = DbClass.DbClass().getDataFromDatabaseMetVoorwaarde('media', 'date', dateTime)
    identifier = data[0][0]
    camera.PiCam().start_record(str(identifier))
    return render_template('home.html')


@app.route('/stop_recording')
def stop_recording():
    camera.PiCam().stop_record()
    return render_template('home.html')


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

    return redirect('/')


@app.route('/led')
def led():
    Led.LedLamp(26).flikker(5)

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
    print(result)

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", debug=True)