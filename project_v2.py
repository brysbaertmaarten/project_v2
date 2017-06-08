from flask import Flask, Response, request, redirect, url_for
from flask import render_template
import os
import Servomotor
import led_lamp
import DbClass

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/rotate', methods=['POST'])
def rotate():
    position = 50 #position opvragen uit db
    richting = request.form['richting']
    if richting == "l":
        Servomotor.ServoMotor(19, position).left_rotate()
    elif richting == "r":
        Servomotor.ServoMotor(19, position).right_rotate()
    elif richting == "u":
        Servomotor.ServoMotor(13, position).right_rotate()
    elif richting == "d":
        Servomotor.ServoMotor(13, position).left_rotate()

    return redirect('/')


@app.route('/led')
def led():
    led_lamp.LedLamp().flikker(5)

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