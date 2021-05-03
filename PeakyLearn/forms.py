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

