class Post:
    thread_number = 0

    def __init__(self, title, body):
        Post.thread_number += 1
        self.__thread_id = Post.thread_number
        self.__title = title
        self.__body = body

    def get_thread_id(self):
        return self.__thread_id

    def get_title(self):
        return self.__title

    def get_body(self):
        return self.__body

    def set_thread_id(self, thread_id):
        self.__thread_id = thread_id

    def set_title(self, title):
        self.__title = title

    def set_body(self, body):
        self.__body = body

class Comment:
    comment_number = 0
    def __init__(self, comment):
        Comment.comment_number += 1
        self.__comment_id = Comment.comment_number
        self.__comment = comment

    def get_comment_id(self):
        return self.__comment_id

    def get_comment(self):
        return self.__comment

    def set_comment_id(self, comment_id):
        self.__comment_id = comment_id

    def set_comment(self, comment):
        self.__comment = comment

