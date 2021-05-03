from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('userPage/', views.userPage, name='userPage'),
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
    path('lectures/<str:course_id>', views.lectures, name='lectures'),
    path('educatorCreatedCourses', views.educatorCreatedCourses, name='educatorCreatedCourses'),
    path('addLecture/<str:course_id>', views.addLecture, name='addLecture'),
    path('deleteCourse/<str:course_id>', views.deleteCourse, name='deleteCourse'),
    path('updateCourse/<str:course_id>', views.updateCourse, name='updateCourse'),

]