import shelve, onetimepass,os,base64
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    count_id = 0 #default
    check_admin = False
    try: #it ran the first time u run init.py it will create this
        db = shelve.open('storage.db','c')
        count_id = db["Row_ID"] #retrieve count_id

        db.close()
    except:
        print('Error in retrieving Row ID from storage.db')

    def __init__(self, first_name, last_name,nric,race,phone_no,email, gender, password, address_1, address_2,postal_code,check_admin,image_destination,check_image_destination):
        self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')
        User.count_id += 1 #plus 1 everytime
        try:
            db = shelve.open('storage.db','c') # it will run for the next sign up,whenever I create another account, I have to open it again as the previous guy account already db.close()
            User.count_id = db["Row_ID"] #retrieve count_id
            db["Row_ID"] = User.count_id #store it back to row_id
            db.close() #User variable
        except:
            print("Error retrieving Row ID")
        self.__row_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__nric = nric
        self.__race = race
        self.__phone_no = phone_no
        self.__email = email
        self.__gender = gender
        self.__password = password
        self.__address_1 = address_1
        self.__address_2 = address_2
        self.__postal_code = postal_code
        self.__check_admin = check_admin
        self.__image_destination = image_destination
        self.__check_image_destination = check_image_destination



    #Accessor Method
    def get_row_id(self):
        return self.__row_id
    def get_first_name(self):
        return self.__first_name
    def get_last_name(self):
        return self.__last_name
    def get_nric(self):
        return self.__nric
    def get_race(self):
        return self.__race
    def get_phone_no(self):
        return self.__phone_no
    def get_email(self):
        return self.__email
    def get_gender(self):
        return self.__gender
    def get_password(self):
        return self.__password
    def get_address_1(self):
        return self.__address_1
    def get_address_2(self):
        return self.__address_2
    def get_postal_code(self):
        return self.__postal_code
    def get_check_admin(self):
        return self.__check_admin
    def get_image_destination(self):
        return self.__image_destination
    def get_check_image_destination(self):
        return self.__check_image_destination

    #Mutator Method
    def set_user_id(self,user_id):
        self.__user_id = user_id
    def set_first_name(self,first_name):
        self.__first_name = first_name
    def set_last_name(self,last_name):
        self.__last_name= last_name
    def set_nric(self, nric):
        self.__nric = nric
    def set_race(self,race):
        self.__race = race
    def set_phone_no(self,phone_no):
        self.__phone_no = phone_no
    def set_email(self, email):
        self.__email = email
    def set_gender(self,gender):
        self.__gender = gender

    def set_address_1(self,address_1):
        self.__address_1 = address_1
    def set_address_2(self,address_2):
        self.__address_2 = address_2
    def set_postal_code(self,postal_code):
        self.__postal_code = postal_code
    def set_check_admin(self,admin):
        self.__check_admin = admin
    def set_image_destination(self,image_destination):
        self.__image_destination = image_destination
    def set_check_image_destination(self,check_image_destination):
        self.__check_image_destination = check_image_destination

    def set_password(self, password):
        self.__password = generate_password_hash(password, method = 'sha256')
    def verify_password(self, password):
        return check_password_hash(self.__password, password)

    def get_totp_uri(self):
        return 'otpauth://totp/2FA-Demo:{0}?secret={1}&issuer=Angel' \
            .format(self.__first_name, self.otp_secret)
    def verify_totp(self, otptoken):
        return onetimepass.valid_totp(otptoken, self.otp_secret)
