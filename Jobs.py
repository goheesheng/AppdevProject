import shelve

class Jobs:
    count_no = 0

    def __init__(self, name, location, job_type, timing, salary):
        Jobs.count_no += 1
        self.__count_no = Jobs.count_no
        self.__name = name
        self.__location = location
        self.__job_type = job_type
        self.__timing = timing
        self.__salary = salary

    def get_count_no(self):
        return self.__count_no

    def get_name(self):
        return self.__name

    def get_location(self):
        return self.__location

    def get_job_type(self):
        return self.__job_type

    def get_timing(self):
        return self.__timing

    def get_salary(self):
        return self.__salary

    def set_name(self, name):
        self.__name = name

    def set_location(self, location):
        self.__location = location

    def set_job_type(self, job_type):
        self.__job_type = job_type

    def set_timing(self, timing):
        self.__timing = timing

    def set_salary(self, salary):
        self.__salary = salary
