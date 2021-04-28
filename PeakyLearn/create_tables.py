import sqlite3
from sqlite3 import Error


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


if __name__=='__main__':

    exec_query('CREATE TABLE IF NOT EXISTS user(\
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                username VARCHAR(50) UNIQUE NOT NULL,\
                password VARCHAR(50) NOT NULL,\
                registerDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\
                firstName VARCHAR(50) NOT NULL,\
                lastName VARCHAR(50) NOT NULL,\
                email VARCHAR(50) NOT NULL,\
                phone VARCHAR(50));')

    exec_query('CREATE TABLE IF NOT EXISTS admin(\
                admin_id INTEGER PRIMARY KEY,\
                FOREIGN KEY (admin_id) REFERENCES user(user_id));')

    exec_query('CREATE TABLE IF NOT EXISTS educator(\
                educator_id INTEGER PRIMARY KEY,\
                wallet INTEGER NOT NULL,\
                FOREIGN KEY (educator_id) REFERENCES user(user_id));')

    exec_query('CREATE TABLE IF NOT EXISTS student(\
                student_id INTEGER PRIMARY KEY,\
                level INTEGER,\
                FOREIGN KEY (student_id) REFERENCES user(user_id));')

    exec_query('CREATE TABLE IF NOT EXISTS course(\
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                courseName VARCHAR(50) NOT NULL,\
                category VARCHAR(50) NOT NULL,\
                price INTEGER,\
                lec_cnt INTEGER,\
                certificate_id VARCHAR(50) NOT NULL,\
                rate INTEGER NOT NULL,\
                edu_id INTEGER NOT NULL,\
                language VARCHAR(20) NOT NULL,\
                FOREIGN KEY (edu_id) REFERENCES educator(educator_id));')

    exec_query('CREATE TABLE IF NOT EXISTS lecture(\
                lecture_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                lecName VARCHAR(50),\
                prereq BOOLEAN);')

    exec_query('CREATE TABLE IF NOT EXISTS note(\
                note_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                s_id INTEGER,\
                c_id INTEGER,\
                content VARCHAR(32765),\
                FOREIGN KEY (s_id) REFERENCES student(student_id),\
                FOREIGN KEY (c_id) REFERENCES course(course_id));')

    exec_query('CREATE TABLE IF NOT EXISTS question(\
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                q_content VARCHAR(32765));')

    exec_query('CREATE TABLE IF NOT EXISTS quiz(\
                quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                quiz_question VARCHAR(32765),\
                answer VARCHAR(32765));')

    exec_query('CREATE TABLE IF NOT EXISTS exam(\
                exam_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                exam_question VARCHAR(32765),\
                exam_answer VARCHAR(32765));')

    exec_query('CREATE TABLE IF NOT EXISTS certificate(\
                certificate_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                type VARCHAR(50));')

    exec_query('CREATE TABLE IF NOT EXISTS refundRequest(\
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                studentID INTEGER,\
                courseID INTEGER,\
                req_content VARCHAR(32765),\
                FOREIGN KEY (studentID) REFERENCES student(studentID),\
                FOREIGN KEY (courseID) REFERENCES course(courseID));')

    exec_query('CREATE TABLE IF NOT EXISTS wishlist(\
                list_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                c_id INTEGER,\
                FOREIGN KEY (c_id) REFERENCES course(course_id));')

    exec_query('CREATE TABLE IF NOT EXISTS decide(\
                adminID INTEGER NOT NULL,\
                requestID INTEGER NOT NULL,\
                response VARCHAR(300),\
                FOREIGN KEY (adminID) REFERENCES admin(admin_id),\
                FOREIGN KEY (requestID) REFERENCES course(request_id));')

    exec_query('CREATE TABLE IF NOT EXISTS complaint(\
                s_id INTEGER NOT NULL,\
                c_id INTEGER NOT NULL,\
                request_id INTEGER NOT NULL,\
                date DATE,\
                FOREIGN KEY (request_id) REFERENCES admin(admin_id),\
                FOREIGN KEY (s_id) REFERENCES student(student_id),\
                FOREIGN KEY (c_id) REFERENCES course(course_id));')

    exec_query('CREATE TABLE IF NOT EXISTS gain(\
                s_id INTEGER NOT NULL,\
                cert_id INTEGER NOT NULL,\
                e_id INTEGER NOT NULL,\
                finish BOOLEAN,\
                FOREIGN KEY (s_id) REFERENCES student(studentID),\
                FOREIGN KEY (cert_id) REFERENCES certificate(certificate_id),\
                FOREIGN KEY (e_id) REFERENCES exam(exam_id));')

    exec_query('CREATE TABLE IF NOT EXISTS has(\
                cert_id INTEGER NOT NULL,\
                course_id INTEGER NOT NULL,\
                FOREIGN KEY (course_id) REFERENCES course(course_id),\
                FOREIGN KEY (cert_id) REFERENCES certificate(certificate_id));')

    exec_query('CREATE TABLE IF NOT EXISTS creates(\
                course_id INTEGER NOT NULL,\
                edu_id INTEGER NOT NULL,\
                FOREIGN KEY (course_id) REFERENCES course(course_id),\
                FOREIGN KEY (edu_id) REFERENCES educator(educator_id));')

    exec_query('CREATE TABLE IF NOT EXISTS contain(\
                course_id INTEGER NOT NULL,\
                lec_id INTEGER NOT NULL,\
                FOREIGN KEY (course_id) REFERENCES course(course_id),\
                FOREIGN KEY (lec_id) REFERENCES lecture(lecture_id));')

    exec_query('CREATE TABLE IF NOT EXISTS on_t(\
                note_id INTEGER NOT NULL,\
                lec_id INTEGER NOT NULL,\
                FOREIGN KEY (note_id) REFERENCES note(note_id),\
                FOREIGN KEY (lec_id) REFERENCES lecture(lecture_id));')

    exec_query('CREATE TABLE IF NOT EXISTS answer(\
                a_date DATE,\
                q_id INTEGER NOT NULL,\
                edu_id INTEGER NOT NULL,\
                FOREIGN KEY (q_id) REFERENCES question(question_id),\
                FOREIGN KEY (edu_id) REFERENCES educator(educator_id));')

    exec_query('CREATE TABLE IF NOT EXISTS take(\
                date DATE,\
                s_id INTEGER NOT NULL,\
                note_id INTEGER NOT NULL,\
                FOREIGN KEY (s_id) REFERENCES student(student_id),\
                FOREIGN KEY (note_id) REFERENCES note(note_id));')

    exec_query('CREATE TABLE IF NOT EXISTS ask(\
                q_date DATE,\
                q_id INTEGER NOT NULL,\
                s_id INTEGER NOT NULL,\
                FOREIGN KEY (s_id) REFERENCES student(student_id),\
                FOREIGN KEY (q_id) REFERENCES question(question_id));')

    exec_query('CREATE TABLE IF NOT EXISTS  pass_t(\
                s_id INTEGER NOT NULL,\
                lec_id INTEGER NOT NULL,\
                quiz_id INTEGER NOT NULL,\
                success BOOLEAN NOT NULL,\
                FOREIGN KEY (s_id) REFERENCES student(student_id),\
                FOREIGN KEY (lec_id) REFERENCES lecture(lecture_id),\
                FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id));')

    exec_query('CREATE TABLE IF NOT EXISTS have(\
                s_id INTEGER NOT NULL,\
                list_id INTEGER NOT NULL,\
                FOREIGN KEY (s_id) REFERENCES student(student_id),\
                FOREIGN KEY (list_id) REFERENCES wishlist(list_id));')

    exec_query('CREATE TABLE IF NOT EXISTS include(\
                c_id INTEGER NOT NULL,\
                list_id INTEGER NOT NULL,\
                FOREIGN KEY (c_id) REFERENCES course(course_id),\
                FOREIGN KEY (list_id) REFERENCES wishlist(list_id));')




























