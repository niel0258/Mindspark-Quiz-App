
#Base class
class Question:
    def __init__(self):
        self.qTitle = ""
        self.subj_name = ""
        self.qType = ""
        self.question = ""
        self.type = ""
        self.right_answer = None   # index of the correct choice, None = not chosen
        self.points = 0
 
 
class MultipleChoice(Question):
    def __init__(self):
        super().__init__()
        self.qType = "Multiple_Choice"
        self.choices = []
 
 
class TrueOrFalse(Question):
    def __init__(self):
        super().__init__()
        self.qType = "True_or_False"
        self.choices = ["True", "False"]