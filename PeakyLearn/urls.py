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
    path('deleteNotes/<str:course_id>/<str:note_id>/', views.deleteNotes, name='deleteNotes'),

    path('addToWishlist/<str:course_id>', views.addToWishlist, name='addToWishlist'),
    path('buyCourse/<str:pk>', views.buyCourse, name='buyCourse'),

    path('quizPage/<str:course_id>', views.quizPage, name='quizPage'),
    path('createQuiz/<str:course_id>', views.createQuiz, name='createQuiz'),

    path('userPage/', views.userPage, name='userPage'),

    path('addReview/<str:course_id>', views.addReview, name='addReview'),

    path('certificateList/', views.certificateList, name='certificateList'),

    path('certificate/<str:pk>', views.certificate, name='certificate'),

    path('seeCourseReviews/<str:course_id>', views.seeCourseReviews, name='seeCourseReviews'),

]