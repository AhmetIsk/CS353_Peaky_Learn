from django import forms

class UserForm(forms.Form):
    email = forms.EmailField(max_length=254)
    fname = forms.CharField(max_length=30)
    lname = forms.CharField(max_length=30)
    uname = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)
    pw = forms.CharField(widget=forms.PasswordInput())

    def get_fields(self):
        return { 'email': self.email, 'fname': self.fname, 'lname': self.lname,
              'uname': self.uname, 'phone': self.phone, 'pw': self.pw }

class AddCourseForm(forms.Form):
    courseName = forms.CharField(max_length= 50, label = "Course Name")
    category = forms.CharField(max_length= 50, label = "Category - Topic")
    price = forms.CharField(max_length= 50,label = "Price")
    language = forms.CharField(max_length= 50, label = "Language")

    values = {

            'courseName' : courseName,
            'category' : category,
            'price' : price,
            'language' : language

    }

class UpdateCourseForm(forms.Form):
    courseName = forms.CharField(max_length= 50, label = "Change Course Name")
    category = forms.CharField(max_length= 50, label = "Change Category - Topic")
    price = forms.CharField(max_length= 50,label = "Change Price")
    language = forms.CharField(max_length= 50, label = "Change Language")

    values = {

            'courseName' : courseName,
            'category' : category,
            'price' : price,
            'language' : language

    }

class LectureForm(forms.Form):
    lecName = forms.CharField(max_length= 50, label="Lecture Name")
    lec_url = forms.URLField(label = "Lecture URL")
    prereq = forms.BooleanField(label="Prerequisite")

    values = {
            'lecName': lecName,
            'lec_url': lec_url,
            'prereq': prereq,
    }

class AddNote(forms.Form):
    content = forms.CharField(max_length=10000, label="Note")

    values = {
        'content': content,
    }

class CreateQuiz(forms.Form):
    quiz_question = forms.CharField(max_length= 1000, label = "Your Question:")
    choiceA = forms.CharField(max_length = 1000, label = "A:")
    choiceB = forms.CharField(max_length = 1000, label = "B:")
    choiceC = forms.CharField(max_length = 1000, label = "C:")
    answer = forms.CharField(max_length = 10, label = "Answer:")

    values = {
        'quiz_question' : quiz_question,
        'choiceA' : choiceA,
        'choiceB' : choiceB,
        'choiceC' : choiceC,
        'answer' : answer,
    }


class QuizForm(forms.Form):
    CHOICES = (('a','a'),
               ('b','b'),
               ('c','c'),
               ('d','d'),)
    picked = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple())


