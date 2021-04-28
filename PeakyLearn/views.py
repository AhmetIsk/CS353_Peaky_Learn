import sqlite3
from sqlite3 import Error

from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages

# Create your views here.
def home(request):
    context = {}
    return render(request, 'PeakyLearn/home.html', context)


def create_connection(db_file='db.sqlite3'):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def exec_query(sql_query):
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute(sql_query)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)



def login(request):
    if request.method == 'POST':
        ""
        exec_query('CREATE TABLE user(\
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                        username VARCHAR(50) UNIQUE NOT NULL,\
                        password VARCHAR(50) NOT NULL,\
                        registerDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
                        firstName VARCHAR(50) NOT NULL,\
                        lastName VARCHAR(50) NOT NULL,\
                        email VARCHAR(50) NOT NULL,\
                        phone VARCHAR(50));')
        ""
        username = request.POST.get('username')
        password = request.POST.get('password')

        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        params = [username, password]
        cursor.execute("SELECT username FROM user WHERE username=? AND password=?", params)

        auth = cursor.fetchone()
        success = 1 if auth else 0
        print("Username=", username, "Password=", password)
        print('Success=', success)
        context = {'username': username}
        if success == 1:
            return render(request, 'PeakyLearn/userPage.html', context)
        else:
            return render(request, 'PeakyLearn/login.html', {})
    elif request.method == 'GET':
        return render(request, 'PeakyLearn/login.html', {})

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('email')
            print(name)

            query = "INSERT INTO user (username, password, firstName, lastName, email, phone) VALUES (?, ?, ?, ?, ?, ?);"

            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            params = [form.cleaned_data.get('uname'), form.cleaned_data.get('pw'), form.cleaned_data.get('fname'),
                      form.cleaned_data.get('lname'), form.cleaned_data.get('email'), form.cleaned_data.get('phone')]
            try:
                cursor.execute(query, params)
            except sqlite3.IntegrityError:
                return HttpResponse('Username already exists!', status=409)

            connection.commit()
            connection.close()

            return HttpResponse("Registration Succesful. Sign in: <a href='/login'>Login</a>")

    elif request.method == 'GET':
        form = UserForm()
        context = { 'form': form }
        return render( request, 'PeakyLearn/signup.html', context )


def userLogout(request):
    context = {}
    logout(request)
    messages.success(request,"Logout Succesful")
    return render( request, 'PeakyLearn/home.html', context )


def courseDetails(request):
    context = {}
    return render(request, 'PeakyLearn/courseDetails.html', context)


