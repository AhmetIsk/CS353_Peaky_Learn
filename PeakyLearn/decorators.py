from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
import sqlite3


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


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if not request.session.get('uid'):
                return redirect('home')

            uid = request.session['uid']
            user_type = get_user_type(uid)
            role_dict = {1: 'educator', 2: 'student', 3: 'admin'}

            if role_dict[user_type] in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.info(request, 'You do not have permission!')
                return redirect('userPage')
                # return HttpResponse('You do not have permission.')

        return wrapper_func

    return decorator
