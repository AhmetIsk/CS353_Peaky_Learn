from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('studentMainPage/', views.studentMainPage, name='studentMainPage'),
    path('signup/<str:type>', views.signup, name='signup'),
    path('courseDetails/<str:pk>', views.courseDetails, name='courseDetails'),
    path('userLogout/', views.userLogout, name='logout'),
    path('addCourse/', views.addCourse, name='addCourse'),
    path('adminMainPage/', views.adminMainPage, name='adminMainPage'),
    path('educatorMainPage/', views.educatorMainPage, name='educatorMainPage'),
    path('educatorMainPage/', views.educatorMainPage, name='educatorMainPage'),
    path('ownedCourses/', views.ownedCourses, name='ownedCourses'),
    path('purchaseCourse/<str:pk>', views.purchaseCourse, name='purchaseCourse'),
    path('studentProfile/<str:pk>', views.purchaseCourse, name='studentProfile'),
    path('educatorProfile/<str:pk>', views.purchaseCourse, name='educatorProfile'),
    path('deleteUser/<str:pk>', views.deleteUser, name='deleteUser'),

    path('studentLectures/<str:course_id>', views.student_lectures, name='studentLectures'),
    path('educatorLectures/<str:course_id>', views.educator_lectures, name='educatorLectures'),

    path('educatorCreatedCourses', views.educatorCreatedCourses, name='educatorCreatedCourses'),
    path('studentProfile/', views.studentProfile, name='studentProfile'),
    path('shoppingCart/', views.shoppingCart, name='shoppingCart'),
    path('addLecture/<str:course_id>', views.addLecture, name='addLecture'),
    path('deleteCourse/<str:course_id>', views.deleteCourse, name='deleteCourse'),

    path('updateCourse/<str:course_id>', views.updateCourse, name='updateCourse'),
    path('notes/<str:course_id>/<str:lecture_id>/', views.notes, name='notes'),
    path('takeNote/<str:course_id>/<str:lecture_id>/', views.takeNote, name='takeNote'),
    path('deleteNotes/<str:note_id>/', views.deleteNotes, name='deleteNotes'),

    path('addToWishlist/<str:course_id>', views.addToWishlist, name='addToWishlist'),
    path('buyCourse/<str:pk>', views.buyCourse, name='buyCourse'),

    path('finalExamPage/<str:course_id>', views.finalExamPage, name='finalExamPage'),

    path('userPage/', views.userPage, name='userPage'),

    path('addReview/<str:course_id>', views.addReview, name='addReview'),

    path('studentCertificates/', views.studentCertificates, name='studentCertificates'),

    path('certificate/<str:pk>', views.certificate, name='certificate'),

    path('seeCourseReviews/<str:course_id>', views.seeCourseReviews, name='seeCourseReviews'),
    path('seeFinalExam/<str:course_id>', views.seeFinalExam, name='seeFinalExam'),
    path('addFinalQuestion/<str:course_id>', views.addFinalQuestion, name='addFinalQuestion'),
    path('deleteFinalQuestion/<str:question_id>/<str:course_id>', views.deleteFinalQuestion, name='deleteFinalQuestion'),
    path('updateFinalQuestion/<str:question_id>/<str:course_id>', views.updateFinalQuestion, name='updateFinalQuestion'),

    path('add_quiz_question/<str:lec_id>/', views.add_quiz_question, name='add_quiz_question'),

    path('eduSeeQuiz/<str:lec_id>/', views.eduSeeQuiz, name='eduSeeQuiz'),
    path('quizPage/<str:lec_id>', views.quizPage, name='quizPage'),
    path('deleteQuizQuestion/<str:question_id>/<str:lec_id>', views.deleteQuizQuestion, name='deleteQuizQuestion'),
    path('updateQuizQuestion/<str:question_id>/<str:lec_id>', views.updateQuizQuestion, name='updateQuizQuestion'),
    path('refundReqStudent/<str:course_id>', views.refundReqStudent, name='refundReqStudent'),

    path('searchCourse/', views.searchCourse, name='searchCourse'),


    path('ask_question/<str:course_id>', views.ask_question, name='ask_question'),
    path('course_q_edu/<str:course_id>', views.course_q_edu, name='course_q_edu'),

    path('answer_q/<str:q_id>/<str:course_id>', views.answer_q, name='answer_q'),
    path('student_questions/<str:course_id>', views.student_questions, name='student_questions'),
    path('make_announcement/<str:course_id>', views.make_announcement, name='make_announcement'),

     path('refundRequestShow/', views.refundRequestShow, name='refundRequestShow'),

    path('refundReqShowAdmin/', views.refundReqShowAdmin, name='refundReqShowAdmin'),
    path('acceptRefundRequest/<str:student_id>/<str:course_id>', views.acceptRefundRequest, name='acceptRefundRequest'),

]