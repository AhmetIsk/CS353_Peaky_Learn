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
    price = forms.IntegerField(min_value=0, label = "Price")
    language = forms.CharField(max_length= 50, label = "Language")
    description = forms.CharField(max_length= 1000, label = "Description")

    values = {

            'courseName' : courseName,
            'category' : category,
            'price' : price,
            'language' : language,
            'description' : description

    }

class UpdateCourseForm(forms.Form):


    courseName = forms.CharField(max_length= 50, label = "Change Course Name",initial='courseName')
    category = forms.CharField(max_length= 50, label = "Change Category - Topic")
    price = forms.CharField(max_length= 50,label = "Change Price")
    language = forms.CharField(max_length= 50, label = "Change Language")
    description = forms.CharField(max_length= 1000, label = "Description")

    values = {

            'courseName' : courseName,
            'category' : category,
            'price' : price,
            'language' : language,
            'description' : description

    }

class LectureForm(forms.Form):
    lecName = forms.CharField(max_length= 50, label="Lecture Name")
    lec_url = forms.URLField(label = "Lecture URL")
    prereq = forms.BooleanField(label="Please accept the terms and conditions.")

    values = {
            'lecName': lecName,
            'lec_url': lec_url,
            'prereq': prereq,
    }

class AddNote(forms.Form):
    content = forms.CharField(max_length=10000, label="")

    values = {
        'content': content,
    }

class AddFinalQuestion(forms.Form):
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
    rating = forms.DecimalField(max_digits=5, decimal_places=1, label="Rate from 1 to 5:")

    values = {
        'r_content': r_content,
        'rating': rating
    }

class RefundRequestForm(forms.Form):
    req_content = forms.CharField(max_length=10000, label="Write your reason for your refund request")

    value = {
        'req_content' : req_content
    }


class DiscountRequestForm(forms.Form):
    req_content = forms.CharField(max_length=10000, label="Convince the admin to make a discount.")
    discount_rate = forms.IntegerField(min_value=0, max_value=100, label="Write your desired discount percentage.")

    value = {
        'req_content': req_content,
        'discount_rate': discount_rate,
    }


class QuizForm(forms.Form):
    __name__ = "quizform"
    #choice = forms.IntegerField(min_value=1, max_value=5, label="Find the correct answer (1='A', 2='B', 3='C', 4='D', 5='E'):")
    CHOICES = ((1, 'a'),
               (2, 'b'),
               (3, 'c'),
               (4, 'd'),
               (5, 'e'))
    picked = forms.ChoiceField(choices=CHOICES)


class AskQuestionForm(forms.Form):
    q_content = forms.CharField(max_length=10000, label="Write your Q/A for the course.")

    value = {
        'q_content': q_content
    }


class AnnouncementForm(forms.Form):
    q_content = forms.CharField(max_length=10000, label="Write your announcement for the course.")

    value = {
        'q_content': q_content
    }


