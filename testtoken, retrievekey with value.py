import os, shelve
import base64
from io import BytesIO
from flask import Flask, render_template, redirect, url_for, flash, session, \
    abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
import onetimepass
import pyqrcode, pyotp

# class Test:
#     def __init__(self,name,email,password):
#         self.__email = email
#         self.__name = name
#         self.__password = password
#     def get_email(self):
#         return self.__email
#     def get_password(self):
#         return self.__password
#     def get_name(self):
#         return self.__name
# def id():
#     nric = next(nric for nric, user in users_dict.items() if user.get_email() == 'a@email.com')
#     return nric
# test = Test('john','a@email.com','niama')
# users_dict = {'123':test}
# id()
# print(id())
#

app = Flask(__name__)
totp = pyotp.TOTP('base32secret3232')
totp.now() # => '492039'
pyotp.totp.TOTP('JBSWY3DPEHPK3PXP').provisioning_uri(name='alice@google.com', issuer_name='Secure App')
# OTP verified for current time
totp.verify('492039') # => True
# time.sleep(30)
totp.verify('492039') # => False
@app.route('/twofactor')
def two_factor_setup():
    # if 'username' not in session:
    #     return redirect(url_for('index'))
    # user = User.query.filter_by(username=session['username']).first()
    # if user is None:
    #     return redirect(url_for('index'))
    # # since this page contains the sensitive qrcode, make sure the browser
    # # does not cache it
    return render_template('two-factor-setup.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
def qrcode():
    if 'username' not in session:
        abort(404)
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        abort(404)

    # for added security, remove username from session
    del session['username']

    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

if __name__ == '__main__':
    app.run(debug=True)
