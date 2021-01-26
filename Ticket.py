from datetime import datetime


class Ticket:
    count_id = 00

    def __init__(self, name, category, subject, message):
        Ticket.count_id += 1
        self.__ticket_id = Ticket.count_id
        self.__name = name
        self.__category = category
        self.__subject = subject
        self.__message = message

    def get_ticket_id(self):
        return self.__ticket_id

    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def get_subject(self):
        return self.__subject

    def get_message(self):
        return self.__message

    def set_ticket_id(self, ticket_id):
        self.__ticket_id = ticket_id

    def set_name(self, name):
        self.__name = name

    def set_category(self, category):
        self.__category = category

    def set_subject(self, subject):
        self.__subject = subject

    def set_message(self, message):
        self.__message = message

    def get_datetime(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        return (dt_string)
