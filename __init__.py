from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, \
    abort
from Forms import CreateUserForm
from Forms2 import CreateTicketForm
from FBForms import CreateFeedbackForm
from ReplyForm import CreateReplyForm
from Login import LoginForm, LoginVerify, LoginEmailVerify
from User import User
from PWReset import PWReset, PWConfirm
from AdminUpdateForm import Admin_UpdateUserForm
from flask_mail import Mail, Message
import Customer
from Thread import CreateThreadForm
from Thread import CreateCommentForm
import shelve, pyotp, onetimepass, pyqrcode, Ticket, Feedback, Reply
import os, base64
from io import BytesIO
import shelve, Jobs
from CreateJobForm import CreateJobForm

# print(os.urandom(24)) generated for line btm 3rd line
app = Flask(__name__)
app.secret_key = '\xc7_\xc4\xdf\x05$\xce\x06\xa8\xd7\x83\xdd\x8d\xae\x92\xd1`\x1e\x04\x01\xbe\xdd\x02\xf6'

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcSED4aAAAAAIa6rWWLbnka0jIkCRNt43IwOp-V'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcSED4aAAAAAJxrdazygAQhvmyjyaZm7HI-n3Pw'

# when user submit the button, this path is used for uploading the image
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='appdevescip2003@gmail.com',
    MAIL_PASSWORD='appdev7181',  # need pw if not the stupid error come out again
    MAIL_DEBUG=True,
    MAIL_SUPPRESS_SEND=False,
    MAIL_ASCII_ATTACHMENTS=True,
)

mail = Mail(app)


@app.route('/twofactor')
def two_factor_setup():
    if 'current_user' not in session:
        return redirect(url_for('home'))
    # user = User.query.filter_by(username=session['username']).first()

    user = session['current_user']

    print(user, '12333333333333333333333333333333333333333')
    if user is None:
        return redirect(url_for('home'))
    # since this page contains the sensitive qrcode, make sure the browser
    # does not cache it
    return render_template('two-factor-setup.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
def qrcode():
    users_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
    except:
        print("Error in retrieving Users from storage.db.")
    if 'current_user' not in session:
        abort(404)
    user = users_dict[session['current_user']]
    print(user, 'an object')
    if user is None:
        abort(404)

    # for added security, remove username from session
    del session['current_user']

    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/home')  # requesting from get method
def home():
    users_dict = {}
    name = ''
    if session["logged_in"] == True and session['Head_Admin'] == False:  # and details.get_check_admin() == True
        try:
            db = shelve.open('storage.db', 'r')
            users_dict = db['Users']
            db.close()
        except:
            print("Error in retrieving Users from storage.db.")
        current_user = users_dict[session['current_user']]  # retrieve key
        if current_user.get_check_admin() == True:
            session['admin'] = True
        if 'admin' in session and session['admin']:

            flash(" Admin Login Successful!")
            details = session['admin']

            current_user = users_dict[session['current_user']]  # retrieve key
            name = current_user.get_first_name()
            print('adminimagecheck', current_user.get_check_image_destination())
            if current_user.get_check_image_destination() == True:  # must always check for typo especically ()
                session['profile_pic'] = True
            elif current_user.get_check_image_destination() == False:
                session['profile_pic'] = False
            current_user = users_dict[session['current_user']]  # retrieve key
            name = current_user.get_first_name()
            print('admin imagecheckdestination', current_user.get_image_destination())
            print(session['profile_pic'], 'admin session check')
            print('session admin =', session['admin'])
            print('check', current_user.get_check_admin())
            return render_template('home.html', currentuser=name, user=details, check_admin=details,
                                   profile_pic=current_user.get_image_destination())
        else:
            try:
                db = shelve.open('storage.db', 'r')
                users_dict = db['Users']
                db.close()
            except:
                print("Error in retrieving Users from storage.db.")
            flash("User Login Successful!")
            session['admin'] = False
            print('imagecheck', current_user.get_check_image_destination())
            if current_user.get_check_image_destination() == True:  # must always check for typo especically ()
                session['profile_pic'] = True
            elif current_user.get_check_image_destination() == False:
                session['profile_pic'] = False
            current_user = users_dict[session['current_user']]  # retrieve key
            name = current_user.get_first_name()
            print('imagecheckdestination', current_user.get_image_destination())
            print(session['profile_pic'], 'session check')
            return render_template('home.html', currentuser=name, profile_pic=current_user.get_image_destination())
    elif session["logged_in"] == True and session['Head_Admin'] == True:
        id = session['current_user']
        return render_template('home.html', currentuser=id)  # to retrieve to html & display out (jinja code thing)
    return render_template('home.html')


@app.route('/')  # requesting from get method
def base():
    return render_template('base.html')


# how to add /<string:nric> ??
# 2 methods
# you must have nric on the client side that can be retrieved out
# since i did not return at server side, i add it into client side
# then just add / string:nric and must add nric into parameter
# benefit is that you dont have to keep on returning on server side

# for update_user, i return nric = user.get_nric() to client side
# so i can still add /<string:nric> and rmb to add in nric to parameter

# must add get method to to retrieve url
@app.route("/upload/<string:nric>", methods=["GET", "POST"])
def upload(nric):
    users_dict = {}

    db = shelve.open('storage.db', 'c')
    users_dict = db['Users']
    user = users_dict[session['current_user']]

    target = os.path.join(APP_ROOT,
                          'static/assets/img/')  # must be the same as return send_from_directory route, this is to set the image into this directory
    print(target)
    # if not inside, then will auto download to the path static/assets/img
    # to prevent downloading it multiple times if user chooses the same file
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    filename = ''
    # session['profile_pic']  = filename
    if request.files.getlist("file") == []:
        # user.set_image_destination('default.png')
        pass
    else:
        for upload in request.files.getlist("file"):
            print(upload)

            filename = upload.filename
            print("{} is the file name".format(upload.filename))
            # This is to verify files are supported
            ext = os.path.splitext(filename)[1]
            if (ext == ".jpg") or (ext == ".png"):
                print("File supported moving on...")
            else:
                print('File NOT supported')
            destination = "/".join([target, filename])
            print("Accept incoming file:", filename)
            print("Save it to:", destination)
            upload.save(destination)
            # filename = session['profile_pic']

        session['profile_pic'] = True
        user.set_check_image_destination(True)
        user.set_image_destination(filename)

    # session['profile_pic'] = filename #store file name back to session

    db["Users"] = users_dict  # very critical, must always store back
    db.close()
    return render_template("customerDetail.html", user=user, currentuser=user.get_first_name(),
                           profile_pic=user.get_image_destination())  # dk why need user = id forget le -.-
    # return send_from_directory("static", filename, as_attachment=True)


# why must i  to set  @app.route('/static/assets/img/<filename>'), cannot be other route
@app.route('/static/assets/img/<filename>')
def send_image(filename):
    return send_from_directory('static/assets/img/', filename)


# it still returns static/assets/img must put
# @app.route('/upload/<filename>')
# def send_image(filename):
#     return send_from_directory('static/assets/img/', filename)

@app.route('/customerDetail/<string:nric>', methods=['GET', 'POST'])
def customerDetail(nric):
    session['logged_in'] = True
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()
    id = session['current_user']
    details = users_dict[id]
    name = details.get_first_name()

    print(details.get_check_admin())
    if details.get_check_admin() == True:
        return render_template('customerDetail.html', currentuser=name, user=details,
                               check_admin=details.get_check_admin())
    elif details.get_check_admin() == False:
        return render_template('customerDetail.html', currentuser=name, user=details)


# remember to create not overide like if nric already have ensure nric cannot be created again
@app.route('/createUser', methods=['GET', 'POST'])  # use post method as behind the scene is HTTPS://
def create_user():
    create_user_form = CreateUserForm(request.form)

    if request.method == 'POST' and create_user_form.validate():
        db = shelve.open('storage.db', 'c')
        users_dict = {}

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")
        if create_user_form.nric.data in users_dict:  # prevent changing data of another existing customer
            flash("NRIC was already created.")
            create_user_form.nric.data = ''
            create_user_form.password.data = ''
        else:
            # Create Object
            user = User(create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.nric.data,
                        create_user_form.race.data, create_user_form.phone_no.data, create_user_form.email.data,
                        create_user_form.gender.data, create_user_form.password.data, create_user_form.address_1.data,
                        create_user_form.address_2.data, create_user_form.postal_code.data, bool(False), '',
                        bool(False))
            # set value as user object with nric as key in user_dict{get_nric: user(object)}
            user.set_password(create_user_form.password.data)
            users_dict[user.get_nric()] = user

            # Put dictionary into shelve/dict with Users as key
            # This will be convinient, like i can add more other segments other than Users.
            db["Users"] = users_dict

            print(user.get_first_name(), user.get_last_name(), "was stored in storage.db successfully with row_id ==",
                  user.get_row_id(), user.get_password())

            db.close()
            session['user_created'] = user.get_first_name() + ' ' + user.get_last_name()
            session['current_user'] = create_user_form.nric.data
            session['logged_in'] = False
            return redirect(url_for(
                'two_factor_setup'))  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~need redirect to twofactor
    return render_template('createUser.html', form=create_user_form)


# add head admin
def add_admin():
    db = shelve.open('storage.db', 'c')
    admin_dict = {}
    try:
        admin_dict = db['Head_Admin']
    except:
        print("Error in retrieving Users from storage.db.")
    while True:
        key = input("Do you want to create Head Admin ID and password? (Y/N)").capitalize()
        if key == "Y":
            admin_id = input("Enter New Head Admin ID: ")
            admin_password = input("Enter New Head Admin Password: ")
            admin_dict[admin_id] = admin_password
            db['Head_Admin'] = admin_dict
            print(admin_dict)
            print('Successful creating Head Admin')
            key = input("Do you want to more create Admin ID and password? (Y/N)").capitalize()
            if key == "N":
                break
            elif key == 'Delete':
                try:
                    key = input("Enter the Head Admin ID to delete: ")
                    user = admin_dict.pop(key)
                    db['Users'] = admin_dict
                    print(f"{key} was removed as Head Admin.")
                except:
                    print('No such admin')
            elif key == "Y":
                admin_id = input("Enter New Head Admin ID: ")
                admin_password = input("Enter New Head Admin Password: ")
                admin_dict[admin_id] = admin_password
                db['Head_Admin'] = admin_dict
                print(admin_dict)
            else:
                print("Please enter Y or N or Delete only!")
                continue
        elif key == "N":
            break
        elif key == 'Delete':
            try:
                key = input("Enter the Head Admin ID to delete: ")
                user = admin_dict.pop(key)
                db['Users'] = admin_dict
                print(f"{key} was removed as Head Admin.")
            except:
                print('No such admin')
        else:
            print("Please enter Y or N or Delete only!")
            continue


@app.route('/logout', methods=["GET", "POST"])
def log_out():
    session['current_user'] = None
    session['Head_Admin'] = None
    session['admin'] = False
    session['logged_in'] = False
    session['profile_pic'] = False
    return redirect(url_for('home'))


@app.route('/chooseVerificationPath//EmailLoginVerifyCode/<string:nric>', methods=["GET", "POST"])
def EmailLoginVerifyCode(nric):
    email_verify_form = LoginEmailVerify(request.form)
    users_dict = {}
    email_data = []  # email = [0],first_name = [1]
    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
    except:
        print("Error retrieving user from storage.db")
    session['logged_in'] = False
    user = users_dict[nric]
    email = user.get_email()
    first_name = user.get_first_name()
    email_data.append(email)
    email_data.append(first_name)
    msg = Message('Login Confirmation', sender='appdevescip2003@gmail.com',
                  recipients=[email_data[0]])  # need put anther square bracket as will have string concatenation error
    msg.html = render_template('email.html', postID='login verify', first_name=email_data[1], token=otp)
    mail.send(msg)
    print(email_data[0])
    print('Sent successful!')
    if request.method == 'POST' and email_verify_form.validate():
        print('test sent')
        if email_verify_form.email_validCode.data == otp:
            session['logged_in'] = True
            return redirect(url_for('home'))  # this nric returns to userChangePW approute<string:nric>
        else:
            flash("Invalid verification code")
    return render_template('EmailLoginVerifyCode.html', form=email_verify_form)


@app.route('/chooseVerificationPath/PhoneLoginVerifyCode/<string:nric>', methods=["GET", "POST"])
def PhoneVerificationPath(nric):
    phone_verify_form = LoginVerify(request.form)
    users_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
    except:
        print("Error retrieving user from storage.db")
    if request.method == 'POST' and phone_verify_form.validate():
        print(nric, 'key1231289378912879312789321789123897312987312')
        key = users_dict[nric]
        if key.verify_totp(
                phone_verify_form.phone_token.data):  # It means you're trying to convert something to JSON that python doesn't know how to convert to JSON
            print('phone otp verified')
            print(key.verify_totp(phone_verify_form.phone_token.data))
            session['logged_in'] = True
            session[
                'current_user'] = nric  # show name on navbar #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MUST NOT STORE SESSION AS OBJECT, if not got Typeerror: Object of type User is not JSON serializable
            session['Head_Admin'] = False  # To ensure this account isn't admin
            return redirect(url_for("home"))
        else:
            flash('Incorrect one time password', 'otp')

    return render_template('PhoneLoginVerifyCode.html', form=phone_verify_form)


@app.route('/chooseVerificationPath/<string:nric>', methods=["GET", "POST"])
def chooseVerificationPath(nric):
    return render_template('chooseVerificationPath.html', nric=nric)  # always need return out so other page can use


@app.route('/login', methods=["GET", "POST"])
def login_page():
    login_form = LoginForm(request.form)
    email_data = []  # email = [0],first_name = [1]
    if request.method == 'POST' and login_form.validate():
        # separate to check whether admin is inside, if not there will be an error retrieving users_dict = db["Users"] as there isnt any customer details inside
        # so i can create admin only then login with admin
        try:
            admin_dict = {}
            db = shelve.open('storage.db', 'r')
            admin_dict = db["Head_Admin"]
            db.close()
            print(admin_dict)
            for key, value in admin_dict.items():
                print(key)
                print(value)
                if login_form.nric.data == key and value == login_form.password.data:  # no object so just put value
                    print("Head Admin Login Successful")
                    flash('Head Admin Login Successful', 'info')
                    session['logged_in'] = True
                    session['current_user'] = key  # there isn't any object, thus = key
                    session['Head_Admin'] = True

                    return redirect(url_for(
                        'retrieve_users'))  # redirect(url_for(), url must be the function instead of the app.route
        except:
            print("Error in retrieving Admin from storage.db.")

        # Retrieve the users_dict object from shelve using the 'Users' key.
        users_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            users_dict = db['Users']
            db.close()
        except:
            print("Error retrieving user from storage.db")
        for key, value in users_dict.items():  # value is object
            password = value.get_password()
            nric = value.get_nric()
            email = value.get_email()
            first_name = value.get_first_name()
            print(password)
            # cannot password == value.verify_password(str(login_form.password.data)) as it is a boolean thus always not the same, so just check True or Not
            if login_form.nric.data == key and value.verify_password(
                    str(login_form.password.data)):  # cannot this method
                session['logged_in'] = False
                session['current_user'] = key  # show name on navbar
                session['Head_Admin'] = False  # To ensure this account isn't admin

                return redirect(url_for('chooseVerificationPath',
                                        nric=login_form.nric.data))  # no need retrieve_users.html as have url_for(), nric is for the app route <string:nric>
        else:
            print("Incorrect username and/or password")
            flash('Incorrect username and/or password', 'info')
            return redirect(url_for('login_page'))

    # print(session['current_user']) test
    return render_template('login.html', form=login_form)  # need at users_list = users_list?


# create otp
def token():
    base32secret = pyotp.random_base32()
    print('Secret:', base32secret)

    totp = pyotp.TOTP(base32secret)
    print('OTP code:', totp.now())
    return totp.now()


@app.route('/verifyCode/<string:email>', methods=["GET", "POST"])
def verify_code(email):
    reset_form = PWReset(request.form)
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()
    session['logged_in'] = False
    if request.method == 'POST' and 'enter-verification-code' in request.form and reset_form.validate:
        if reset_form.email_validCode.data == otp:
            session['logged_in'] = True
            for key in users_dict:
                if users_dict[key].get_email() == email:
                    nric = key
                    return redirect(
                        url_for('userChangePW', nric=nric))  # this nric returns to userChangePW approute<string:nric>
        else:
            flash("Invalid verification code")
    return render_template('verifyCode.html', form=reset_form)


# send mail
@app.route('/forgetPassword', methods=["GET", "POST"])
def reset_pw():
    session["logged_in"] = False  # keep this for now,
    reset_form = PWReset(request.form)
    email_data = []  # email = [0],first_name = [1]
    db = shelve.open('storage.db', 'r')
    users_dict = db['Users']
    db.close()
    if request.method == 'POST' and 'send-verification-code' in request.form and reset_form.validate:
        # try:
        for key, value in users_dict.items():  # value is object
            email = value.get_email()
            first_name = value.get_first_name()
            if reset_form.email.data == email:  # will check user_dict emails if got such email, it is == as it is in for loop thus checking each email 1 by 1
                email_data.append(email)
                email_data.append(first_name)
                msg = Message('Reset password', sender='appdevescip2003@gmail.com', recipients=[
                    email_data[0]])  # need put anther square bracket as will have string concatenation error
                msg.html = render_template('email.html', postID='reset password', first_name=email_data[1], token=otp)
                mail.send(msg)
                print('Sent successful!')
                return redirect(url_for('verify_code',
                                        email=reset_form.email.data))  # need to have email for def verify_code email app route
        else:
            flash("No such email, did you create an account?")
    return render_template('forgetPassword.html', form=reset_form,
                           token=otp)  # cannot put this token = token() as will generate again as i called the function again


# incomplete
@app.route('/userChangePW/<string:nric>', methods=["GET", "POST"])
def userChangePW(nric):
    session['logged_in'] = False
    confirm_form = PWConfirm(request.form)
    if request.method == 'POST' and confirm_form.validate():
        db = shelve.open('storage.db', 'c')
        users_dict = {}

        users_dict = db['Users']
        user = users_dict.get(nric)
        user.set_password(confirm_form.password.data)
        db['Users'] = users_dict
        db.close()
        flash("Password Successfully Changed")  # not working dk why
        return redirect(url_for('home'))
    return render_template('userChangePW.html', form=confirm_form, nric=nric)


@app.route('/retrieveUsers')
def retrieve_users():
    users_list = []
    users_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
    except:
        print("Error in retrieving Users from storage.db.")
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)
    if session['Head_Admin'] == True:
        id = session['current_user']  # id = 'admin'
        return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list,
                               currentuser=id)  # to retrieve to html & display out (jinja code thing)
    id = session['current_user']
    details = users_dict[id]
    name = details.get_first_name()

    if session['Head_Admin'] == False and details.get_check_admin() == True:
        # get_key = users_dict[session['current_user']] # retrieve object from session['current_user'] which is a key
        return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list, currentuser=name,
                               user=details, check_admin=details.get_check_admin(),
                               profile_pic=details.get_image_destination())  # to retrieve to html & display out (jinja code thing)
    elif session['Head_Admin'] == False and details.get_check_admin() == False:
        return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list, currentuser=name,
                               user=details)


##session['admin'] == True/ False is not required as only Head Admin can choose whether you can be a moderator
@app.route('/updateUser/<string:nric>/', methods=['GET', 'POST'])
def update_user(nric):
    update_user_form = Admin_UpdateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate() and session[
        'Head_Admin'] == True:  # POST method, update upon clicking submission
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(nric)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_race(update_user_form.race.data)
        user.set_phone_no(update_user_form.phone_no.data)
        user.set_email(update_user_form.email.data)
        user.set_gender(update_user_form.gender.data)
        if update_user_form.password.data == '' and update_user_form.confirm_password.data == '':
            print('did not update ')
            pass
        else:
            user.set_password(update_user_form.password.data)
            print('updated')
        user.set_address_1(update_user_form.address_1.data)
        user.set_address_2(update_user_form.address_2.data)
        user.set_postal_code(update_user_form.postal_code.data)
        user.set_check_admin(update_user_form.become_admin.data)
        print(user.get_check_admin())
        db['Users'] = users_dict
        db.close()

        session['user_updated'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('retrieve_users'))


    # to retrieve data from shelve and diplay previous data
    # so bascially this will come first as admin did not click update thus post doesnt work first
    elif request.method == 'POST' and update_user_form.validate() and session['Head_Admin'] == False:  # customer side
        if session['admin']:
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Users']

            user = users_dict.get(nric)
            user.set_first_name(update_user_form.first_name.data)
            user.set_last_name(update_user_form.last_name.data)
            user.set_race(update_user_form.race.data)
            user.set_phone_no(update_user_form.phone_no.data)
            user.set_email(update_user_form.email.data)
            user.set_gender(update_user_form.gender.data)
            if update_user_form.password.data == '' and update_user_form.confirm_password.data == '':
                print('did not update/ ')
                pass
            else:
                user.set_password(update_user_form.password.data)
            print('updated')
            user.set_address_1(update_user_form.address_1.data)
            user.set_address_2(update_user_form.address_2.data)
            user.set_postal_code(update_user_form.postal_code.data)

            db['Users'] = users_dict
            db.close()
            session['user_updated'] = user.get_first_name() + ' ' + user.get_last_name()

            return redirect(url_for('retrieve_users'))
        elif session['admin'] == False:
            users_dict = {}
            db = shelve.open('storage.db', 'w')
            users_dict = db['Users']

            user = users_dict.get(nric)
            user.set_first_name(update_user_form.first_name.data)
            user.set_last_name(update_user_form.last_name.data)
            user.set_race(update_user_form.race.data)
            user.set_phone_no(update_user_form.phone_no.data)
            user.set_email(update_user_form.email.data)
            user.set_gender(update_user_form.gender.data)
            # if nothing is filled in the webpage, password will not be changed
            if update_user_form.password.data == '' and update_user_form.confirm_password.data == '':
                print('did not update/ ')
                pass
            else:
                user.set_password(update_user_form.password.data)
            user.set_address_1(update_user_form.address_1.data)
            user.set_address_2(update_user_form.address_2.data)
            user.set_postal_code(update_user_form.postal_code.data)

            db['Users'] = users_dict
            db.close()
            session['user_updated'] = user.get_first_name() + ' ' + user.get_last_name()

            return redirect(url_for('upload', nric=nric))

    elif request.method == 'GET' and session['Head_Admin'] == False:  # get method
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(nric)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.race.data = user.get_race()
        update_user_form.phone_no.data = user.get_phone_no()
        update_user_form.email.data = user.get_email()
        update_user_form.gender.data = user.get_gender()

        update_user_form.address_1.data = user.get_address_1()
        update_user_form.address_2.data = user.get_address_2()
        update_user_form.postal_code.data = user.get_postal_code()

    elif request.method == 'GET' and session['Head_Admin'] == True:  # get method
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(nric)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.race.data = user.get_race()
        update_user_form.phone_no.data = user.get_phone_no()
        update_user_form.email.data = user.get_email()
        update_user_form.gender.data = user.get_gender()
        update_user_form.password.data = user.get_password()
        update_user_form.address_1.data = user.get_address_1()
        update_user_form.address_2.data = user.get_address_2()
        update_user_form.postal_code.data = user.get_postal_code()
        update_user_form.become_admin.data = user.get_check_admin()
    users_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
    except:
        print("Error retrieving user")
    user = users_dict.get(nric)
    print(user.get_check_admin())  # check
    if user.get_check_admin() == True:
        user.set_check_admin(True)

    elif user.get_check_admin() == False:
        user.set_check_admin(False)

    if session['Head_Admin'] == True:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(nric)
        id = session['current_user']  # = nric also can
        return render_template('updateUser.html', form=update_user_form, currentuser=id, nric=user.get_nric())
    elif user.get_check_admin() == True:

        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(nric)
        id = session['current_user']  # key of the person who first logged in
        name = users_dict[id].get_first_name()  # to get person who first logged in
        return render_template('updateUser.html', form=update_user_form, currentuser=name, nric=id,
                               check_admin=user.get_check_admin())
    elif user.get_check_admin() == False:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(nric)  # display the customer nric not admin nric
        # bottom 3 is for the nav bar name
        # current user =/= id is because, when Head_Admin login, the nric must still be the customer detail, not the admin id
        user = users_dict.get(nric)
        id = session['current_user']
        print(id)
        name = users_dict[id].get_first_name()
        return render_template('updateUser.html', form=update_user_form, currentuser=name, nric=id)  # show navbar name
    return redirect(url_for('retrieve_users'))


@app.route('/deleteUser/<string:nric>', methods=['POST'])
def delete_user(nric):
    if session['Head_Admin'] == True:
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.pop(nric)

        db['Users'] = users_dict
        db.close()

        session['user_deleted'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('retrieve_users'))
    elif session['Head_Admin'] == False:  # customer return to log out page

        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.pop(nric)

        db['Users'] = users_dict
        db.close()

        session['user_deleted'] = user.get_first_name() + ' ' + user.get_last_name()
        if session['admin'] == False:
            return redirect(url_for('log_out'))
        elif session['admin'] == True:
            return redirect(url_for('retrieve_users'))


@app.route('/createTicket', methods=['GET', 'POST'])
def create_ticket():
    create_ticket_form = CreateTicketForm(request.form)
    if request.method == 'POST' and create_ticket_form.validate() and session['logged_in'] == True:
        tickets_dict = {}
        tickets_count_id = 0
        db = shelve.open('storage.db', 'c')

        try:
            tickets_dict = db['Tickets']
            tickets_count_id = int(db['tickets_count_id'])
        except:
            print("Error in retrieving Inventories from storage.db.")

        ticket = Ticket.Ticket(create_ticket_form.category.data,
                               create_ticket_form.subject.data, create_ticket_form.message.data)

        tickets_count_id += 1
        ticket.set_ticket_id(tickets_count_id)
        db['tickets_count_id'] = tickets_count_id
        tickets_dict[ticket.get_ticket_id()] = ticket
        db['Tickets'] = tickets_dict

        db.close()
        return redirect(url_for('retrieve_tickets'))


    elif session['logged_in'] == False:
        flash('Please Login First')
        return redirect(url_for('login_page'))

    user_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
    except:
        print('Error retrieving ticket')

    id = session['current_user']
    details = users_dict[id]
    name = details.get_first_name()

    return render_template('createTicket.html', form=create_ticket_form, currentuser=name)


@app.route('/retrieveTickets')
def retrieve_tickets():
    tickets_dict = {}
    name = ''
    try:
        db = shelve.open('storage.db', 'r')
        tickets_dict = db['Tickets']
        db.close()
    except:
        print('Error in retrieving ticket from storage.db')

    tickets_list = []
    for key in tickets_dict:
        ticket = tickets_dict.get(key)
        tickets_list.append(ticket)

    flash('New ticket has been created')

    if session['logged_in'] and session['Head_Admin'] == True:
        tickets_dict = {}
        name = ''
        try:
            db = shelve.open('storage.db', 'r')
            tickets_dict = db['Tickets']
            db.close()
        except:
            print('Error in retrieving ticket from storage.db')

        tickets_list = []
        for key in tickets_dict:
            ticket = tickets_dict.get(key)
            tickets_list.append(ticket)
        id = session['current_user']  # id = 'admin'
        return render_template('retrieveTickets.html', count=len(tickets_list), tickets_list=tickets_list,
                               currentuser=id)

    elif session['logged_in'] == False:
        flash('Please Login First')
        return redirect(url_for('login_page'))

    user_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
    except:
        print('Error retrieving tickets')

    id = session['current_user']
    details = users_dict[id]
    name = details.get_first_name()

    return render_template('retrieveTickets.html', count=len(tickets_list), tickets_list=tickets_list, currentuser=name)


@app.route('/updateTicket/<int:id>/', methods=['GET', 'POST'])
def update_ticket(id):
    update_ticket_form = CreateTicketForm(request.form)
    if request.method == 'POST' and update_ticket_form.validate():
        tickets_dict = {}
        db = shelve.open('storage.db', 'w')
        tickets_dict = db['Tickets']

        ticket = tickets_dict.get(id)
        ticket.set_category(update_ticket_form.category.data)
        ticket.set_subject(update_ticket_form.subject.data)
        ticket.set_message(update_ticket_form.message.data)

        db['Tickets'] = tickets_dict
        db.close()

        user_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            users_dict = db['Users']
            db.close()
        except:
            print('Error retrieving tickes')

        id = session['current_user']
        details = users_dict[id]
        name = details.get_first_name()

        return redirect(url_for('retrieve_tickets', currentuser=id))
    else:
        tickets_dict = {}
        db = shelve.open('storage.db', 'r')
        tickets_dict = db['Tickets']
        db.close()

        ticket = tickets_dict.get(id)
        update_ticket_form.category.data = ticket.get_category()
        update_ticket_form.subject.data = ticket.get_subject()
        update_ticket_form.message.data = ticket.get_message()

        user_dict = {}
        try:
            db = shelve.open('storage.db', 'r')
            users_dict = db['Users']
            db.close()
        except:
            print('Error retrieving tickes')

        id = session['current_user']
        details = users_dict[id]
        name = details.get_first_name()

        return render_template('updateTicket.html', form=update_ticket_form, currentuser=id)


@app.route('/deleteTicket/<int:id>', methods=['POST'])
def delete_ticket(id):
    tickets_dict = {}
    db = shelve.open('storage.db', 'w')
    tickets_dict = db['Tickets']

    tickets_dict.pop(id)

    db['Tickets'] = tickets_dict
    db.close()

    return redirect(url_for('retrieve_tickets'))


@app.route('/viewTicket', methods=['GET', 'POST'])
def view_ticket():
    tickets_dict = {}
    db = shelve.open('storage.db', 'r')
    tickets_dict = db['Tickets']
    db.close()

    tickets_list = []
    for key in tickets_dict:
        ticket = tickets_dict.get(key)
        tickets_list.append(ticket)

    create_reply_form = CreateReplyForm(request.form)
    if request.method == 'POST' and create_reply_form.validate():
        replies_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            replies_dict = db['Replies']
        except:
            print('Error in retrieving feedback from storage.db')

        reply = Reply.Reply(create_reply_form.reply.data)
        replies_dict[reply.get_reply_id] = reply
        db['Reply'] = replies_dict
        db.close()

        session['replied'] = reply.get_reply()
        return redirect(url_for('retrieve_tickets'))

    if session['logged_in'] and session['Head_Admin'] == True:
        id = session['current_user']  # id = 'admin'
        return render_template('viewTicket.html', count=len(tickets_list), tickets_list=tickets_list, currentuser=id,
                               form=create_reply_form)

    user_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
    except:
        print('Error retrieving tickes')

    id = session['current_user']
    details = users_dict[id]
    name = details.get_first_name()

    return render_template('viewTicket.html', count=len(tickets_list), tickets_list=tickets_list, currentuser=name,
                           form=create_reply_form)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    create_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and create_feedback_form.validate():
        feedbacks_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            feedbacks_dict = db['Feedbacks']
        except:
            print('Error in retrieving feedback from storage.db')

        feedback = Feedback.Feedback(create_feedback_form.thoughts.data,
                                     create_feedback_form.reason.data,
                                     create_feedback_form.suggestions.data)
        feedbacks_dict[feedback.get_feedback_id] = feedback
        db['Feedbacks'] = feedbacks_dict

    user_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
    except:
        print('Error retrieving tickes')

    id = session['current_user']
    details = users_dict[id]
    name = details.get_first_name()

    return render_template('feedback.html', form=create_feedback_form, currentuser=name)


@app.route('/viewReply')
def view_reply():
    replies_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        replies_dict = db['Replies']
        db.close()
    except:
        print('Error in retrieving reply from storage.db')

    replies_list = []
    for key in replies_dict:
        reply = replies_dict.get(key)
        replies_list.append(reply)

    user_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
    except:
        print('Error retrieving tickets')

    id = session['current_user']
    details = users_dict[id]
    name = details.get_first_name()

    return render_template('viewReply.html', count=len(replies_list), replies_list=replies_list, currentuser=name)

@app.route('/jobCreate', methods=['GET', 'POST'])
def create_job():
    create_job_form = CreateJobForm(request.form)
    if request.method == 'POST' and create_job_form.validate():
        jobs_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            jobs_dict = db['Jobs']
        except:
            print("Error in retrieving Jobs from storage.db.")

        job = Jobs.Jobs(create_job_form.name.data, create_job_form.location.data, create_job_form.job_type.data, create_job_form.timing.data, create_job_form.salary.data)
        jobs_dict[job.get_count_no()] = job
        db['Jobs'] = jobs_dict

        db.close()

        return redirect(url_for('retrieve_jobs'))
    return render_template('jobCreate.html', form=create_job_form)

@app.route('/jobRetrieve')
def retrieve_jobs():
    jobs_dict = {}

    db = shelve.open('storage.db', 'r')
    jobs_dict = db['Jobs']
    db.close()

    # users_dict = {}
    # db = shelve.open('storage.db', 'r')
    # users_dict = db['Users']
    # db.close()
    #
    # user = users_dict.get(nric)
    # id = session['current_user']  # key of the person who first logged in

    jobs_list = []
    for key in jobs_dict:
        job = jobs_dict.get(key)
        jobs_list.append(job)

    return render_template('jobRetrieve.html',count=len(jobs_list), jobs_list=jobs_list)

@app.route('/jobSearch')
def search_jobs():
    if session['logged_in'] == True:
        jobs_dict = {}
        db = shelve.open('storage.db', 'r')
        jobs_dict = db['Jobs']
        db.close()

        jobs_list = []
        for key in jobs_dict:
            job = jobs_dict.get(key)
            jobs_list.append(job)

    elif session['logged_in'] == False:
        flash('Please Login First')
        return redirect(url_for('login_page'))

    return render_template('jobSearch.html',count=len(jobs_list), jobs_list=jobs_list)

@app.route('/jobUpdate/<int:no>/', methods=['GET', 'POST'])
def update_job(no):
    update_job_form = CreateJobForm(request.form)
    if request.method == 'POST' and update_job_form.validate():
        jobs_dict = {}
        db = shelve.open('storage.db', 'w')
        jobs_dict = db['Jobs']

        job = jobs_dict.get(no)
        job.set_name(update_job_form.name.data)
        job.set_location(update_job_form.location.data)
        job.set_job_type(update_job_form.job_type.data)
        job.set_timing(update_job_form.timing.data)
        job.set_salary(update_job_form.salary.data)

        db['Jobs'] = jobs_dict
        db.close()

        return redirect(url_for('retrieve_jobs'))
    else:
        jobs_dict = {}
        db = shelve.open('storage.db', 'r')
        jobs_dict = db['Jobs']
        db.close()

        job = jobs_dict.get(no)
        update_job_form.name.data = job.get_name()
        update_job_form.location.data = job.get_location()
        update_job_form.job_type.data = job.get_job_type()
        update_job_form.timing.data = job.get_timing()
        update_job_form.salary.data = job.get_salary()

        return render_template('jobUpdate.html', form=update_job_form)

@app.route('/deleteJob/<int:no>', methods=['POST'])
def delete_job(no):
    jobs_dict = {}
    db = shelve.open('storage.db', 'w')
    jobs_dict = db['Jobs']

    jobs_dict.pop(no)

    db['Jobs'] = jobs_dict
    db.close()

    return redirect(url_for('retrieve_jobs'))

@app.route('/Forum')
def forum():
    post_dict = {}
    db = shelve.open('forumStorage.db', 'c')
    post_dict = db['Post']
    db.close()

    post_list = []
    for key in post_dict:
        Post = post_dict.get(key)
        post_list.append(Post)

    return render_template('Forum.html', count=len(post_list), post_list=post_list)

@app.route('/CreateThread', methods=['GET', 'POST'])
def create_thread():
    create_thread_form = CreateThreadForm(request.form)
    if request.method == 'POST' and create_thread_form.validate():

        post_dict = {}
        db = shelve.open('forumStorage.db', 'w')

        try:
            post_dict = db['Post']
        except:
            print("Error in retrieving Post from storage.db.")

        post = Customer.Post(create_thread_form.title.data, create_thread_form.body.data)
        post_dict[post.get_thread_id()] = post
        db['Post'] = post_dict

        db.close()

        return redirect(url_for('forum'))
    return render_template('createThread.html', form=create_thread_form)

@app.route('/delete_post/<int:id>', methods=['POST'])
def delete_post(id):
    forum_dict = {}
    db = shelve.open('forumStorage.db', 'w')
    forum_dict = db['Post']

    forum_dict.pop(id)

    db['Post'] = forum_dict
    db.close()

    return redirect(request.referrer)

@app.route('/editUser/<int:id>/', methods=['GET', 'POST'])
def edit_thread(id):
    edit_user_thread = CreateThreadForm(request.form)
    if request.method == 'POST' and edit_user_thread.validate():
        db = shelve.open('forumStorage.db', 'w')
        users_dict = db['Post']

        user = users_dict.get(id)
        user.set_title(edit_user_thread.title.data)
        user.set_body(edit_user_thread.body.data)
        db['Post'] = users_dict
        db.close()

        return redirect(url_for('forum'))
    else:
        users_dict = {}
        db = shelve.open('forumStorage.db', 'r')
        users_dict = db['Post']
        db.close()

        thread = users_dict.get(id)
        edit_user_thread.title.data = thread.get_title()
        edit_user_thread.body.data = thread.get_body()

        return render_template('editUser.html', form=edit_user_thread)

@app.route('/Comment/<int:id>/', methods=['GET', 'POST'])
def add_comment(id):
    create_user_comment = CreateCommentForm(request.form)
    post_dict = {}
    db = shelve.open('forumStorage.db', 'w')
    post_dict = db['Post']
    comment_dict = {}

    if 'comment' in db:
        comment_dict = db['comment']
    db.close()
    Post = post_dict.get(id)
    comment_list = []
    for key in comment_dict:
        Comment = comment_dict.get(key)
        comment_list.append(Comment)

    if request.method == 'POST' and create_user_comment.validate():

        comment_dict = {}
        db = shelve.open('forumStorage.db', 'c')
        try:
            comment_dict = db['comment']
        except:
            print("Error in retrieving Post from storage.db.")

        Comment = Customer.Comment(create_user_comment.comment.data)
        comment_dict[Comment.get_comment()] = Comment
        db['comment'] = comment_dict

        db.close()

        return redirect(url_for('add_comment', id=id))
    return render_template('comment.html', form=create_user_comment, Post=Post, comment_list=comment_list)

@app.route('/delete_comment/<id>', methods=['POST'])
def delete_comment(id):
    comment_dict = {}
    db = shelve.open('forumStorage.db', 'w')
    comment_dict = db['comment']
    comment_dict.pop(id)

    db['comment'] = comment_dict
    db.close()

    return redirect(request.referrer)

if __name__ == '__main__':
    # can use type delete to delete Head Admin Accounts
    add_admin()
    otp = token()
    app.run(debug=True)  # run twice cuz debug built in system bla bla bla
