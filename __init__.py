from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm
import shelve, FormResponse

app = Flask(__name__)
WTF_CRSF_SECRET_KEY = 'a random string'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/covidForm', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(csrf_enabled=False)
    if request.method == 'POST' and create_user_form.validate_on_submit():
        users_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        user = FormResponse.User(create_user_form.first_name.data, create_user_form.last_name.data, create_user_form.email.data, create_user_form.jobs.data, create_user_form.date.data, create_user_form.time.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        # Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_first_name(), user.get_last_name(), "was stored in storage.db successfully with user_id ==", user.get_user_id())

        db.close()


        return redirect(url_for('home'))
    return render_template('covidForm.html', form=create_user_form)

@app.route('/retrieveBooking')
def retrieve_users():
    users_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
    except:
        users_list = []
    else:
        users_dict = db['Users']
        db.close()

        users_list = []
        for key in users_dict:
            user = users_dict.get(key)
            users_list.append(user)

    return render_template('retrieveBooking.html', count=len(users_list), users_list=users_list)

@app.route('/updateBooking/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form, csrf_enabled=False)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('storage.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_email(update_user_form.email.data)
        user.set_job(update_user_form.jobs.data)
        user.set_date(update_user_form.date.data)
        user.set_time(update_user_form.time.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.email.data = user.get_email()
        update_user_form.jobs.data = user.get_job()
        update_user_form.date.data = user.get_date()
        update_user_form.time.data = user.get_time()

        return render_template('updateBooking.html', form=update_user_form)

@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('storage.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_booking'))



if __name__ == '__main__':
    app.run()

