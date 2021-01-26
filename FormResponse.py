class User:
    count_id = 0

    def __init__(self, first_name, last_name, email, job, date, time):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__job = job
        self.__date = date
        self.__time = time

    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_job(self):
        return self.__job

    def get_date(self):
        return self.__date

    def get_time(self):
        return self.__time

    def set_user_id(self,user_id):
        self.__user_id = user_id

    def set_first_name(self,first_name):
        self.__frist_name = first_name

    def set_last_name(self,last_name):
        self.__last_name = last_name

    def set_email(self,email):
        self.__email = email

    def set_job(self,job):
        self.__job = job

    def set_date(self,date):
        self.__date = date

    def set_time(self,time):
        self.__time = time


