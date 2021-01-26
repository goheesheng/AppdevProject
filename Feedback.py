class Feedback:

    def __init__(self, thoughts, reason, suggestions):
        self.__feedback_id = None
        self.__thoughts = thoughts
        self.__reason = reason
        self.__suggestions = suggestions

    def get_thoughts(self):
        return self.__thoughts
    def get_reason(self):
        return self.__reason
    def get_suggestions(self):
        return self.__suggestions
    def get_feedback_id(self):
        return self.__feedback_id()

    def set_thought(self,thoughts):
        self.__thoughts = thoughts
    def set_reason(self,reason):
        self.__reason = reason
    def set_suggestions(self,suggestions):
        self.__suggestions = suggestions
