from django import forms
from django.core.validators import MaxValueValidator


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

            'coursneName' : courseName,
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
    choiceD = forms.CharField(max_length=1000, label="D:")
    choiceE = forms.CharField(max_length=1000, label="E:")
    answer = forms.IntegerField(min_value=1, max_value=5, label="Correct answer (1='A', 2='B', 3='C', 4='D', 5='E'):")

    values = {
        'quiz_question' : quiz_question,
        'choiceA' : choiceA,
        'choiceB' : choiceB,
        'choiceC' : choiceC,
        'choiceD': choiceD,
        'choiceE': choiceE,
        'answer' : answer,
    }

class AddReview(forms.Form):
    r_content = forms.CharField(max_length=10000, label="Comments on this course")
    rating = forms.IntegerField(min_value=1, max_value=5, label="Rate from 1 to 5:")

    values = {
        'r_content': r_content,
        'rating': rating
    }


class QuizForm(forms.Form):
    #choice = forms.IntegerField(min_value=1, max_value=5, label="Find the correct answer (1='A', 2='B', 3='C', 4='D', 5='E'):")
    CHOICES = ((1, 'a'),
               (2, 'b'),
               (3, 'c'),
               (4, 'd'),
               (5, 'e'))
    picked = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple())


