class Reply:
    count_id = 00

    def __init__(self, reply):
        Reply.count_id += 1
        self.__reply_id = Reply.count_id
        self.__reply = reply

    def get_reply(self):
        return self.__reply

    def get_reply_id(self):
        return self.__reply_id

    def set_reply(self, reply):
        self.__reply = reply

    def set_reply_id(self, reply_id):
        self.__reply_id = reply_id
