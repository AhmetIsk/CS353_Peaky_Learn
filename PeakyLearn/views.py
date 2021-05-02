import sqlite3
from sqlite3 import Error

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm, AddCourseForm

from django.contrib.auth import logout
from django.contrib import messages

from .create_tables import create_all

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
        create_all()

        username = request.POST.get('username')
        password = request.POST.get('password')

        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        params = [username, password]
        cursor.execute("SELECT user_id FROM user WHERE username=? AND password=?", params)

        auth = cursor.fetchone()
        success = 1 if auth else 0

        if success == 1:

            # Check the user type
            id = auth[0]
            params = [id]
            cursor.execute("SELECT * FROM student WHERE student_id = ?;", params)
            is_student = cursor.fetchone()
            s = 1 if is_student else 0

            request.session['username'] = username
            request.session['uid'] = auth[0]

            if s:
                request.session['userType'] = 'student'
                return redirect('userPage')
            else:
                request.session['userType'] = 'educator'
                return redirect('educatorMainPage')
        else:
            messages.info(request, 'Wrong username or password.')
            return render(request, 'PeakyLearn/login.html', {})
    elif request.method == 'GET':
        return render(request, 'PeakyLearn/login.html', {})

# Type = 1 -> educator
# Type = 2 -> student
def signup(request, type):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            if type == '2':  # Student
                query = "INSERT INTO user (username, password, firstName, lastName, email, phone) VALUES (?, ?, ?, ?, ?, ?);"

                connection = sqlite3.connect('db.sqlite3')
                cursor = connection.cursor()
                params = [form.cleaned_data.get('uname'), form.cleaned_data.get('pw'), form.cleaned_data.get('fname'),
                          form.cleaned_data.get('lname'), form.cleaned_data.get('email'), form.cleaned_data.get('phone')]
                try:
                    cursor.execute(query, params)
                except sqlite3.IntegrityError:
                    messages.info(request, 'This student already exists!')
                    return redirect('signup', type=2)

                connection.commit()
                connection.close()

                # Get the id of the newly added user
                query = "SELECT user_id FROM user WHERE username = ?;"
                params = [form.cleaned_data.get('uname')]

                connection = sqlite3.connect('db.sqlite3')
                cursor = connection.cursor()

                try:
                    cursor.execute(query, params)
                except sqlite3.IntegrityError:
                    messages.info(request, 'Unsuccessful fetch!')
                    return redirect('signup', type=2)

                id = cursor.fetchone()

                query = "INSERT INTO student (student_id, level) VALUES (?, ?);"
                params = [id[0], 0]

                try:
                    cursor.execute(query, params)
                except sqlite3.IntegrityError:
                    messages.info(request, 'Unsuccessful student insert!')
                    return redirect('signup', type=2)

                connection.commit()
                connection.close()

                messages.info(request, 'Registration of Student {} is Succesful.'.format(form.cleaned_data.get('uname')))
                return redirect('login')
            elif type == '1':  # Educator
                query = "INSERT INTO user (username, password, firstName, lastName, email, phone) VALUES (?, ?, ?, ?, ?, ?);"

                connection = sqlite3.connect('db.sqlite3')
                cursor = connection.cursor()
                params = [form.cleaned_data.get('uname'), form.cleaned_data.get('pw'), form.cleaned_data.get('fname'),
                          form.cleaned_data.get('lname'), form.cleaned_data.get('email'),
                          form.cleaned_data.get('phone')]
                try:
                    cursor.execute(query, params)
                except sqlite3.IntegrityError:
                    messages.info(request, 'This educator already exists!')
                    return redirect('signup', type=1)

                connection.commit()
                connection.close()

                # Get the id of the newly added user
                query = "SELECT user_id FROM user WHERE username = ?;"
                params = [form.cleaned_data.get('uname')]

                connection = sqlite3.connect('db.sqlite3')
                cursor = connection.cursor()

                try:
                    cursor.execute(query, params)
                except sqlite3.IntegrityError:
                    messages.info(request, 'Unsuccessful fetch!')
                    return redirect('signup', type=1)

                id = cursor.fetchone()

                query = "INSERT INTO educator (educator_id, wallet) VALUES (?, ?);"
                params = [id[0], 1000]

                try:
                    cursor.execute(query, params)
                except sqlite3.IntegrityError:
                    messages.info(request, 'Unsuccessful educator insert!')
                    return redirect('signup', type=1)

                connection.commit()
                connection.close()

                messages.info(request,
                              'Registration of Educator {} is Succesful.'.format(form.cleaned_data.get('uname')))
                return redirect('login')
        else:
            return HttpResponse("Invalid form!")

    elif request.method == 'GET':
        create_all()
        form = UserForm()
        context = {'form': form}
        return render(request, 'PeakyLearn/signup.html', context)

# Insert some items for testing
def default_insert():
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    query = "INSERT INTO course (courseName, category, price, language, lec_cnt, certificate_id, rate, edu_id) VALUES (?,?,?,?,?,?,?,?);"
    params = ['CS101', 'CS', 4, 'Eng', 4, 0, 0, 0 ]

    cursor.execute(query, params)

    connection.commit()
    connection.close()


def get_owned_courses(uid):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    params = [uid]
    print(uid)
    query = "SELECT * FROM course WHERE course_id IN (SELECT course_id FROM buy WHERE student_id = ?);"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in get_owned_courses', status=404)

    courses = cursor.fetchall()
    connection.close()

    print(courses)
    return courses

def get_all_courses():
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    query = "SELECT * FROM course;"
    try:
        cursor.execute(query)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in get_all_courses', status=404)

    courses = cursor.fetchall()
    connection.close()

    return courses

def ownedCourses(request):
    owned_courses = get_owned_courses(request.session['uid'])

    context = { 'owned_courses': owned_courses }
    return render(request, 'PeakyLearn/ownedCourses.html', context)


def userPage(request):
    #default_insert()
    uname = request.session['username']

    all_courses = get_all_courses()

    context = {'username': uname, 'all_courses': all_courses }
    return render(request, 'PeakyLearn/userPage.html', context)

def userLogout(request):
    context = {}
    logout(request)
    messages.success(request, "Logout Succesful")
    return render(request, 'PeakyLearn/home.html', context)


def courseDetails(request, pk):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    params = [pk]
    print(pk)
    query = "SELECT * FROM course WHERE course_id = ?;"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in courseDetails', status=404)

    course = cursor.fetchone()
    print(course)
    connection.close()

    context = {'course': course}
    return render(request, 'PeakyLearn/courseDetails.html', context)

def adminMainPage(request):
    context = {}
    return render(request, 'PeakyLearn/adminMainPage.html', context)


def educatorMainPage(request):
    context = {'username': request.session['username']}
    return render(request, 'PeakyLearn/educatorMainPage.html', context)


def addCourse(request):
    if request.method == 'POST':

        form = AddCourseForm(request.POST)
        if form.is_valid():
            courseName = form.cleaned_data.get('courseName')
            category = form.cleaned_data.get('category')
            price = form.cleaned_data.get('price')
            language = form.cleaned_data.get('language')

            query = "INSERT INTO course (courseName, category, price, language, lec_cnt, certificate_id, rate, edu_id) VALUES (?,?,?,?,?,?,?,?);"
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            params2 = [courseName, category, price, language, 0, "1", 0, 0, ]
            try:
                cursor.execute(query, params2)
                print("successful- course created")
            except sqlite3.IntegrityError:
                print("unsuccessful-course is not created")
                # return HttpResponse('Username already exists!', status=409)

            connection.commit()
            connection.close()

            return HttpResponse("Course Creation Succesful. Back to Main: <a href='/educatorMainPage'>Back</a>")

    elif request.method == 'GET':
        form = AddCourseForm()
        context = {'form': form}
        return render(request, 'PeakyLearn/addCourse.html', context)


def purchaseCourse(request, pk):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    uid = request.session['uid']
    params = [pk, uid]
    print(params)

    # First check if the course is already bought
    query = "SELECT * FROM buy WHERE course_id = ? AND student_id = ?;"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in purchaseCourse', status=404)

    course = cursor.fetchone()
    print(course)
    already_bought = 1 if course else 0

    if already_bought:
        return HttpResponse("You have already purchased this course. Back to Main: <a href='/userPage'>Back</a>")

    # Add the course
    params = [pk, uid, 0]
    query = "INSERT INTO buy VALUES( ?, ?, ? )"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in purchaseCourse', status=404)

    connection.commit()
    connection.close()

    return HttpResponse("Success!. Back to Main: <a href='/userPage'>Back</a>")
