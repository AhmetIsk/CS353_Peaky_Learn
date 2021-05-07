import sqlite3
from sqlite3 import Error

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .decorators import allowed_users
from .forms import UserForm, AddCourseForm, LectureForm , UpdateCourseForm, AddNote, QuizForm, CreateQuiz, AddReview

from django.contrib.auth import logout
from django.contrib import messages

from .create_tables import create_all

# Create your views here.
def home(request):
    context = {}
    create_all()
    default_insert()
    return render(request, 'PeakyLearn/home.html', context)


def create_connection(db_file='db.sqlite3'):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def exec_query(sql_query, params):
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute(sql_query, params)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)
        return HttpResponse(e)


# Returns:
# 1 if educator
# 2 if student
# 3 if admin
def get_user_type(uid):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    print("user id:", uid)
    params = [uid]
    cursor.execute("SELECT * FROM student WHERE student_id = ?;", params)
    is_student = cursor.fetchone()
    s = True if is_student else False

    cursor.execute("SELECT * FROM admin WHERE admin_id = ?;", params)
    is_admin = cursor.fetchone()
    s_admin = True if is_admin else False

    if s:
        return 2
    elif s_admin:
        return 3
    else:
        return 1

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
            userid = auth[0]
            user_type = get_user_type(userid)

            request.session['username'] = username
            request.session['uid'] = auth[0]

            if user_type == 2:
                request.session['userType'] = 'student'
                return redirect('studentMainPage')
            elif user_type == 3:
                request.session['userType'] = 'admin'
                return redirect('adminMainPage')
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

    #cursor.execute(query, params)

    #cursor.execute(query, params)
    connection.commit()

    query = "SELECT user_id FROM user WHERE username = 'admin';"
    cursor.execute(query)
    uid = cursor.fetchone()

    if not uid:
        # Add admin
        query = "INSERT INTO user (username, password, firstName, lastName, email, phone) VALUES (?, ?, ?, ?, ?, ?);"
        params = ["admin", "0000", "a", "b", "admin@g.c", "123"]

        cursor.execute(query, params)
        connection.commit()

        query = "INSERT INTO admin (admin_id) VALUES (1);"
        cursor.execute(query)

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

@allowed_users(allowed_roles=['student'])
def ownedCourses(request):
    uname = request.session['username']
    owned_courses = get_owned_courses(request.session['uid'])
    context = {'username': uname, 'owned_courses': owned_courses }
    return render(request, 'PeakyLearn/ownedCourses.html', context)

def get_owned_certificates(uid):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    params = [uid]
    print(uid)
    query = "SELECT * FROM certificate WHERE certificate_id IN (SELECT cert_id FROM gain WHERE s_id=?);"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in get_owned_courses', status=404)

    certificates = cursor.fetchall()
    connection.close()

    print(certificates)
    return certificates


@allowed_users(allowed_roles=['student'])
def studentCertificates(request):
    uname = request.session['username']
    certificates = get_owned_certificates(request.session['uid'])
    context = {'username': uname, 'certificates': certificates}
    return render(request, 'PeakyLearn/certificateList.html', context)

@allowed_users(allowed_roles=['student'])
def certificate(request, pk):
    # ayni sekilde course querysi yerine finished course olusturulabilir yahut finish gibi bir attribute eklenebilir
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
    uname = request.session['username']
    regDate, fname, lname, email, phone = get_user_data(request.session['uid'])
    context = {'username': uname,'course': course, 'fname': fname, 'lname': lname, 'regDate': regDate}
    return render(request, 'PeakyLearn/certificate.html', context)

@allowed_users(allowed_roles=['student'])
def studentMainPage(request):
    uname = request.session['username']

    all_courses = get_all_courses()

    context = {'username': uname, 'all_courses': all_courses }
    return render(request, 'PeakyLearn/studentMainPage.html', context)

@allowed_users(allowed_roles=['student', 'educator', 'admin'])
def userLogout(request):
    context = {}
    logout(request)
    messages.success(request, "Logout Succesful")
    return render(request, 'PeakyLearn/home.html', context)


@allowed_users(allowed_roles=['student', 'educator', 'admin'])
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
    uname = request.session['username']
    context = {'username': uname,'course': course}
    return render(request, 'PeakyLearn/courseDetails.html', context)

@allowed_users(allowed_roles=['student'])
def buyCourse(request, pk):
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
    uname = request.session['username']
    context = {'username': uname,'course': course}
    return render(request, 'PeakyLearn/buyCourse.html', context)

@allowed_users(allowed_roles=['admin'])
def adminMainPage(request):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    query = "SELECT * FROM user;"
    try:
        cursor.execute(query)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in adminpage', status=404)

    all_users = cursor.fetchall()

    query = "SELECT * FROM student;"
    try:
        cursor.execute(query)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in adminpage', status=404)

    students = cursor.fetchall()
    query = "SELECT * FROM educator;"
    try:
        cursor.execute(query)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in adminpage', status=404)
    educators = cursor.fetchall()
    connection.close()

    context = {'students': students, 'educators': educators, 'all_users': all_users}
    return render(request, 'PeakyLearn/adminMainPage.html', context)

@allowed_users(allowed_roles=['educator'])
def educatorMainPage(request):
    context = {'username': request.session['username']}
    all_courses = get_all_courses()

    context = {'username': request.session['username'], 'all_courses': all_courses}
    return render(request, 'PeakyLearn/educatorMainPage.html', context)

def get_user_data(uid):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    query = "SELECT * FROM user WHERE user_id=?;"
    param = [uid]
    try:
        cursor.execute(query, param)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in adminpage', status=404)

    data = cursor.fetchall()[0]
    regDate = data[3]

    fname = data[4]
    lname = data[5]
    email = data[6]
    phone = data[7]
    connection.close()

    return regDate, fname, lname, email, phone

@allowed_users(allowed_roles=['student', 'educator', 'admin'])
def studentProfile(request):
    uname = request.session['username']
    regDate, fname, lname, email, phone = get_user_data(request.session['uid'])
    owned_courses = get_owned_courses(request.session['uid'])
    context = {'username': uname, 'owned_courses': owned_courses, 'fname': fname, 'lname': lname,
               'email': email, 'phone': phone, 'regDate': regDate }
    return render(request, 'PeakyLearn/studentProfile.html', context)

def get_wishlist(uid):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    params = [uid]
    query = "SELECT list_id FROM wishlist WHERE s_id=?"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('Error in wishlist', status=404)

    list_id = cursor.fetchone()

    if not list_id:
        return None

    params = [list_id[0]]

    # now add into include
    query = "SELECT * FROM course WHERE course_id IN (SELECT c_id FROM include WHERE list_id=?);"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('Error in wishlist', status=404)

    wishlist = cursor.fetchall()
    connection.close()
    print(wishlist)

    return wishlist


def shoppingCart(request):
    wishlist = get_wishlist(request.session['uid'])
    context = {'username': request.session['username'], 'wishlist': wishlist}
    return render(request, 'PeakyLearn/shoppingCart.html', context)


@allowed_users(allowed_roles=['educator'])
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
            params = [courseName, category, price, language, 0, "1", 0, request.session['uid'] ]
            try:
                cursor.execute( query, params )
            except sqlite3.IntegrityError as e:
                print(e)
                return HttpResponse('unsuccessful-course is not created!', status=409)

            connection.commit()

            course_id = cursor.lastrowid
            query = "INSERT INTO creates (course_id, edu_id) VALUES (?,?);"
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            params = [course_id, request.session['uid']]
            try:
                cursor.execute(query, params)
            except sqlite3.IntegrityError as e:
                print(e)
                return HttpResponse('unsuccessful-course is not created!', status=409)

            connection.commit()

            # Insert the certificate of the course into db
            params = [course_id]
            query = "SELECT courseName FROM course WHERE course_id=?;"
            cursor.execute(query, params)
            cert_name = cursor.fetchone()[0] + " Certificate"

            query = "INSERT INTO certificate (c_id, cert_name) VALUES (?,?);"
            params = [course_id, cert_name]
            try:
                cursor.execute(query, params)
            except sqlite3.IntegrityError as e:
                print(e)
                return HttpResponse('unsuccessful-course is not created!', status=409)

            connection.commit()
            connection.close()
            
            return HttpResponse("Course Creation Succesful. Back to Main: <a href='/educatorMainPage'>Back</a>")

    elif request.method == 'GET':
        form = AddCourseForm()
        context = {'form': form}
        return render(request, 'PeakyLearn/addCourse.html', context)


@allowed_users(allowed_roles=['educator'])
def addLecture(request, course_id):
    if request.method == 'POST':

        form = LectureForm(request.POST)
        if form.is_valid():
            lecName = form.cleaned_data.get('lecName')
            lec_url = form.cleaned_data.get('lec_url')
            prereq = form.cleaned_data.get('prereq')

            query = "INSERT INTO lecture (lecName, prereq, lec_url) VALUES (?,?,?);"
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            params = [lecName, prereq, lec_url]
            try:
                cursor.execute(query, params)
            except sqlite3.IntegrityError as e:
                print(e)
                return HttpResponse('Cannot add lecture!', status=409)

            connection.commit()
            lec_id = cursor.lastrowid

            query = "INSERT INTO contain (course_id, lec_id) VALUES (?,?);"
            params = [course_id, lec_id]
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            try:
                cursor.execute(query, params)
            except sqlite3.IntegrityError as e:
                print(e)
                return HttpResponse('Cannot add lecture!', status=409)

            connection.commit()
            connection.close()

            return HttpResponse("Lecture Succesfully Added. Back to Main: <a href='/educatorMainPage'>Back</a>")

    elif request.method == 'GET':
        form = LectureForm()
        context = {'form': form}
        return render(request, 'PeakyLearn/addLecture.html', context)

@allowed_users(allowed_roles=['student'])
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
        return HttpResponse("You have already purchased this course. Back to Main: <a href='/studentMainPage'>Back</a>")

    # Add the course
    params = [pk, uid]
    query = "INSERT INTO buy VALUES( ?, ? )"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError:
        return HttpResponse('Error in purchaseCourse', status=404)

    connection.commit()
    connection.close()

    return HttpResponse("Success!. Back to Main: <a href='/studentMainPage'>Back</a>")

@allowed_users(allowed_roles=['admin'])
def deleteUser(request, pk):
    user_type = get_user_type(pk)

    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    #cursor.execute("PRAGMA foreign_keys=ON")
    params = [pk]
    type_str = ""

    if user_type == 3:  # Admin
        connection.close()
        return HttpResponse("Cannot delete admin. Back to Main: <a href='/adminMainPage'>Back</a>")

    print("USER TYPE: ", user_type, " PK: ", pk)

    if user_type == 1:  # edu
        type_str = "educator"
    elif user_type == 2:  # student
        type_str = "student"

    query = "DELETE FROM {} WHERE {}_id = ?;".format(type_str, type_str)

    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('Error in deleteUser', e, status=404)

    # delete user
    query = "DELETE FROM user WHERE user_id = ?;"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('Error in deleteUser', status=404)

    connection.commit()
    connection.close()

    return HttpResponse("Deletion Succesful. Back to Main: <a href='/adminMainPage'>Back</a>")

@allowed_users(allowed_roles=['educator'])
def educator_lectures(request, course_id):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    params = [course_id]
    query = ""
    query = "SELECT * FROM lecture WHERE lecture_id IN (SELECT lec_id FROM contain WHERE course_id=?);"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError:
        return HttpResponse('Error in lectures', status=404)

    lectures = cursor.fetchall()
    connection.close()


    context = {'lectures': lectures, 'course_id': course_id}


    return render(request, 'PeakyLearn/lecturesEducator.html', context)

@allowed_users(allowed_roles=['student'])
def student_lectures(request, course_id):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    params = [request.session['uid'], course_id]
    query = "SELECT * FROM buy WHERE student_id=? AND course_id=?;"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('Error in lectures', status=404)
    bought = cursor.fetchone()
    bought_course = 1 if bought else 0

    if not bought:
        return HttpResponse("You do not own this course. Back to Main: <a href='/userPage'>Back</a>")

    params = [course_id]
    query = "SELECT * FROM lecture WHERE lecture_id IN (SELECT lec_id FROM contain WHERE course_id=?);"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('Error in lectures', status=404)

    lectures = cursor.fetchall()

    query = "SELECT * FROM course WHERE course_id = ?;"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in courseDetails', status=404)

    course = cursor.fetchone()
    print(course)


    uname = request.session['username']

    # TODO: Check if the user is qualified for the final exam. Do this after adding the quizzes.

    # If the user completed this course, the student cannot enter final exam again:
    params = [request.session['uid'], course_id]
    query = "SELECT * FROM gain WHERE s_id=? AND cert_id IN (SELECT certificate_id FROM certificate WHERE c_id=?);"
    cursor.execute(query, params)
    passed = cursor.fetchone()
    passed_course = 1 if passed else 0

    qualified = True
    if passed_course:
        qualified = False

    connection.close()
    context = {'course': course, 'username': uname,
               'lectures': lectures, 'course_id': course_id,
               'qualified': qualified}


    return render(request, 'PeakyLearn/lecturesStudent.html', context)

def get_created_courses(uid):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    params = [uid]
    print(uid)
    query = "SELECT * FROM course WHERE course_id IN (SELECT course_id FROM creates WHERE edu_id = ?);"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError:
        return HttpResponse('404! error in get_owned_courses', status=404)

    courses = cursor.fetchall()
    connection.close()

    print(courses)
    return courses


@allowed_users(allowed_roles=['educator', 'admin'])
def educatorCreatedCourses(request):
    created_courses = get_created_courses(request.session['uid'])
    context = {'created_courses': created_courses, 'username': request.session['username']}
    return render(request, 'PeakyLearn/educatorCreatedCourses.html', context)

@allowed_users(allowed_roles=['educator', 'admin'])
def deleteCourse(request, course_id):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    # delete course
    query = "DELETE FROM course WHERE course_id = ?;"
    params = [course_id]
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('Error in deleteCourse', status=404)

    connection.commit()
    connection.close()

    return HttpResponse("Deletion Succesful. Back to Main: <a href='/educatorMainPage'>Back</a>")

@allowed_users(allowed_roles=['educator', 'admin'])
def updateCourse(request, course_id):

    if request.method == 'POST':

        form = UpdateCourseForm(request.POST)
        if form.is_valid():
            courseName = form.cleaned_data.get('courseName')
            category = form.cleaned_data.get('category')
            price = form.cleaned_data.get('price')
            language = form.cleaned_data.get('language')

            query = "UPDATE course SET courseName = ?, category = ?, price = ?, language = ? WHERE course_id = ?"
            params = [courseName, category, price, language,course_id]
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()

            try:
                cursor.execute( query, params )
            except sqlite3.IntegrityError as e:
                print(e)
                return HttpResponse('unsuccessful-course is not updated!', status=409)

            connection.commit()
            connection.close()
            return HttpResponse("Course is Updated Succesfully. Back to Main: <a href='/educatorMainPage'>Back</a>")

    elif request.method == 'GET':
        form = UpdateCourseForm()
        context = {'form': form, 'course_id': course_id}
        return render(request, 'PeakyLearn/updateCourse.html', context)

@allowed_users(allowed_roles=['student', 'educator', 'admin'])
def takeNote(request, course_id, lecture_id):
    if request.method == 'POST':

        form = AddNote(request.POST)
        if form.is_valid():
            s_id = request.session.get('uid')
            c_id = course_id
            content = form.cleaned_data.get('content')


            query = "INSERT INTO note (s_id, c_id, content) VALUES (?,?,?);"
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            params = [s_id, c_id, content]
            try:
                cursor.execute(query, params)
            except sqlite3.IntegrityError as e:
                print(e)
                return HttpResponse('unsuccessful-note is not created!', status=409)

            connection.commit()

            note_id = cursor.lastrowid

            query = "INSERT INTO take (s_id, note_id) VALUES (?,?);"
            params = [s_id, note_id]
            try:
                cursor.execute(query, params)
            except sqlite3.IntegrityError as e:
                print(e)
                return HttpResponse('unsuccessful-note is not created!', status=409)

            connection.commit()

            query = "INSERT INTO on_t (note_id, lec_id) VALUES (?,?);"
            params = [note_id, lecture_id]
            try:
                cursor.execute(query, params)
            except sqlite3.IntegrityError as e:
                print(e)
                return HttpResponse('unsuccessful-note is not created!', status=409)

            connection.commit()
            connection.close()

            return HttpResponse("Note Creation Succesful. Back to Lectures Page: <a href='/studentLectures/{}'>Back</a>:".format(course_id))

    elif request.method == 'GET':
        form = AddNote()

        # Get course name and lecture name
        query = "SELECT courseName FROM course WHERE course_id=?;"
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        params = [course_id]
        try:
            cursor.execute(query, params)
        except sqlite3.IntegrityError as e:
            print(e)
            return HttpResponse('takenote', status=409)

        course_name = cursor.fetchone()[0]

        query = "SELECT lecName FROM lecture WHERE lecture_id=?;"
        params = [lecture_id]
        try:
            cursor.execute(query, params)
        except sqlite3.IntegrityError as e:
            print(e)
            return HttpResponse('takenote', status=409)

        lecture_name = cursor.fetchone()[0]
        connection.close()

        context = {'form': form, 'c_id': course_id, 'cname':course_name, 'lec_id': lecture_id, 'lec_name': lecture_name}
        return render(request, 'PeakyLearn/takeNote.html', context)

# Returns all of the notes taken by the student in the specifies lecture
def get_all_notes(uid, course_id, lecture_id):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    query = "SELECT * FROM note WHERE c_id=? AND note_id IN (SELECT note_id FROM take NATURAL JOIN on_t WHERE s_id=? AND lec_id=?);"
    params = [course_id, uid, lecture_id]
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('404! error in get_all_courses', status=404)

    my_notes = cursor.fetchall()
    print("Notes: ", my_notes)
    connection.close()

    return my_notes


@allowed_users(allowed_roles=['educator', 'admin', 'student'])
def notes(request, course_id, lecture_id):
    all_notes = get_all_notes(request.session['uid'], course_id, lecture_id)
    print(all_notes)
    context = {'all_notes': all_notes}
    return render(request, 'PeakyLearn/notes.html', context)

@allowed_users(allowed_roles=['educator', 'admin', 'student'])
def addToWishlist(request, course_id):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    uid = request.session['uid']
    params = [course_id, uid]
    print(params)

    # First check if the course is already wishlisted
    query = "SELECT * FROM include WHERE c_id=? AND list_id=(SELECT list_id FROM wishlist WHERE s_id = ?);"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('409! error in wishlist', status=409)

    course = cursor.fetchone()
    print(course)
    already_wishlisted = 1 if course else 0

    if already_wishlisted:
        return HttpResponse("You have already wishlisted this course. Back to Main: <a href='/studentMainPage'>Back</a>")

    # And check if the course is already bought
    query = "SELECT * FROM buy WHERE course_id=? AND student_id=?;"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('409! error in wishlist', status=409)

    course = cursor.fetchone()
    print(course)
    already_bought = 1 if course else 0

    if already_bought:
        return HttpResponse(
            "You have already bought this course. Back to Main: <a href='/studentMainPage'>Back</a>")

    # Add the course into wishlist
    # Create the student's own wishlist, if not created yet
    params = [uid]
    query = "SELECT * FROM wishlist WHERE s_id=?"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('Error in wishlist', status=404)

    wl = cursor.fetchone()
    has_wishlist = 1 if wl else 0

    if not has_wishlist:  # Does not have a wishlist
        params = [uid]
        query = "INSERT INTO wishlist (s_id) VALUES(?)"
        try:
            cursor.execute(query, params)
        except sqlite3.OperationalError as e:
            print(e)
            return HttpResponse('Error in wishlist', status=404)

        connection.commit()
        list_id = cursor.lastrowid

        # now add into include
        query = "INSERT INTO include (list_id, c_id) VALUES(?, ?)"
        params = [list_id, course_id]
        try:
            cursor.execute(query, params)
        except sqlite3.OperationalError as e:
            print(e)
            return HttpResponse('Error in wishlist', status=404)

        connection.commit()
        connection.close()
    else:  # Has a wishlist
        # Get the list id
        params = [uid]
        query = "SELECT list_id FROM wishlist WHERE s_id=?"
        try:
            cursor.execute(query, params)
        except sqlite3.OperationalError as e:
            print(e)
            return HttpResponse('Error in wishlist', status=404)

        list_id = cursor.fetchone()[0]
        params = [list_id, course_id]

        # now add into include
        query = "INSERT INTO include (list_id, c_id) VALUES(?, ?)"
        try:
            cursor.execute(query, params)
        except sqlite3.OperationalError as e:
            print(e)
            return HttpResponse('Error in wishlist', status=404)

        connection.commit()
        connection.close()

    return HttpResponse("Course addded to wishlist!. Back to Main: <a href='/userPage'>Back</a>")

def finalExamPage(request, course_id):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            picked = int(form.cleaned_data.get('picked')[0])

            # Check if the answer is correct
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            params = [course_id]
            print(params)

            # First check if the course is already wishlisted
            query = "SELECT exam_answer FROM final_exam WHERE c_id=?;"
            try:
                cursor.execute(query, params)
            except sqlite3.OperationalError as e:
                print(e)
                return HttpResponse('409! error in wishlist', status=409)

            answer = int(cursor.fetchone()[0])

            if picked == answer:  # Correct choice!
                # Give the student certificate
                uid = request.session['uid']

                # Get certificate id
                param = [course_id]
                query = "SELECT certificate_id FROM certificate WHERE c_id=?"
                cursor.execute(query, param)
                cert_id = cursor.fetchone()[0]

                # Get exam id
                param = [course_id]
                query = "SELECT exam_id FROM final_exam WHERE c_id=?"
                cursor.execute(query, param)
                exam_id = int(cursor.fetchone()[0])

                params = [uid, cert_id, exam_id, True]
                query = "INSERT INTO gain VALUES(?, ?, ?, ?);"
                try:
                    cursor.execute(query, params)
                except sqlite3.OperationalError as e:
                    print(e)
                    return HttpResponse('409! error in wishlist', status=409)

                connection.commit()
                connection.close()

                return HttpResponse("Yay! You have passed the exam and gained your certificate! Back to Main: <a href='/userPage'>Back</a>")
            else:  # Incorrect choice!
                return HttpResponse('Incorrect choice! You need to work more!')
    else:
        form = QuizForm()

        # Get the exam contents:
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        param = [course_id]
        query = "SELECT * FROM final_exam WHERE c_id=?"
        cursor.execute(query, param)
        exam = cursor.fetchone()

        if not exam:
            return HttpResponse("A final quiz has not been created for this course yet. Contact the course owner. Back to Main: <a href='/userPage'>Back</a>")

        connection.close()

        exam_content = exam
        print("EXAM CONTENT:", exam_content)
        context = {'form': form, 'course_id': course_id, 'exam_content': exam_content}
        return render(request, 'PeakyLearn/finalExamPage.html', context)

@allowed_users(allowed_roles=['educator'])
def createFinalExam(request, course_id):

    if request.method == 'POST':
        form = CreateQuiz(request.POST)
        if form.is_valid():

            quiz_question = form.cleaned_data.get('quiz_question')
            choiceA = form.cleaned_data.get('choiceA')
            choiceB = form.cleaned_data.get('choiceB')
            choiceC = form.cleaned_data.get('choiceC')
            choiceD = form.cleaned_data.get('choiceD')
            choiceE = form.cleaned_data.get('choiceE')
            answer = form.cleaned_data.get('answer')

            query = "INSERT INTO final_exam(exam_question, c_id, choiceA, choiceB, choiceC, choiceD, choiceE, exam_answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
            params = [quiz_question, course_id, choiceA, choiceB, choiceC, choiceD, choiceE, answer]
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()

            try:
                cursor.execute(query, params)
            except sqlite3.IntegrityError as e:
                print(e)
                return HttpResponse('unsuccessful-quiz is not created!', status=409)

            connection.commit()
            connection.close()
            return HttpResponse("Exam is Created. Back to Main: <a href='/educatorMainPage'>Back</a>")

    elif request.method == 'GET':
        query = "SELECT * FROM final_exam WHERE c_id=?"
        params = [course_id]
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        cursor.execute(query, params)
        added = cursor.fetchone()
        abort = 1 if added else 0
        if abort:
            return HttpResponse("You can only create a single final exam. Go back: <a href='/educatorMainPage'>Back</a>")


        form = CreateQuiz()
        context = {'form': form, 'course_id': course_id}
        return render(request, 'PeakyLearn/createQuiz.html', context)

@allowed_users(allowed_roles=['student'])
def addReview(request, course_id):

    student_id = request.session['uid']

    # First check if this user submitted a review before
    query = "SELECT * FROM review WHERE s_id=? AND c_id=?;"
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    params = [student_id, course_id]
    try:
        cursor.execute(query, params)
    except sqlite3.IntegrityError as e:
        print(e)
        return HttpResponse('error in review!', status=409)

    exists = cursor.fetchone()
    reviewed_before = 1 if exists else 0

    if reviewed_before:
        return HttpResponse("You have reviewed this course before! Back to Lectures Page: <a href='/ownedCourses/'>Back</a>:")

    if request.method == 'POST':

        form = AddReview(request.POST)
        if form.is_valid():
            s_id = request.session.get('uid')
            c_id = course_id
            r_content = form.cleaned_data.get('r_content')
            rating = form.cleaned_data.get('rating')

            query = "INSERT INTO review (s_id, c_id, r_content, rating) VALUES (?,?,?,?);"
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            params = [s_id, c_id, r_content, rating]
            try:
                cursor.execute(query, params)
            except sqlite3.IntegrityError as e:
                print(e)
                return HttpResponse('unsuccessful-review is not created!', status=409)

            connection.commit()
            connection.close()

            return HttpResponse("Review Creation Succesful. Back to Lectures Page: <a href='/ownedCourses/'>Back</a>:")

    elif request.method == 'GET':
        form = AddReview()

        # Get course name
        query = "SELECT courseName FROM course WHERE course_id=?;"
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        params = [course_id]
        try:
            cursor.execute(query, params)
        except sqlite3.IntegrityError as e:
            print(e)
            return HttpResponse('addreview', status=409)

        course_name = cursor.fetchone()[0]
        connection.close()

        context = {'form': form, 'c_id': course_id, 'cname': course_name}
        return render(request, 'PeakyLearn/review.html', context)

# Redirect into user's page based on user type
@allowed_users(allowed_roles=['educator', 'student', 'admin'])
def userPage(request):
    utype = request.session.get('userType')
    print("utype:", utype)

    if utype == 'student':
        return redirect('studentMainPage')
    elif utype == 'educator':
        return redirect('educatorMainPage')
    else:
        return redirect('adminMainPage')


def get_all_reviews(course_id):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    params = [course_id]
    query = "SELECT * FROM review WHERE c_id=?;"
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('404! error in get_all_reviews', status=404)

    reviews = cursor.fetchall()
    connection.close()
    return reviews

@allowed_users(allowed_roles=['educator', 'admin', 'student'])
def seeCourseReviews(request, course_id):
    all_reviews = get_all_reviews(course_id)
    print(all_reviews)
    avg = 0
    if len(all_reviews) > 0:

        for review in all_reviews:
            avg += review[3]

        avg /= len(all_reviews)

    uname = request.session['username']

    context = {'all_reviews': all_reviews, 'avg_rating': avg, 'username': uname}
    return render(request, 'PeakyLearn/courseReviews.html', context)

def deleteNotes(request, note_id):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    # delete course
    query = "DELETE FROM note WHERE note_id=?;"
    params = [note_id]
    try:
        cursor.execute(query, params)
    except sqlite3.OperationalError as e:
        print(e)
        return HttpResponse('Error in deleteCourse', status=404)

    connection.commit()
    connection.close()

    return HttpResponse("Deletion Succesful. Back to Main: <a href='/studentMainPage'>Back</a>")

#def createComplaint(request, course_id):
