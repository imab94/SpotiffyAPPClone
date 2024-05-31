from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login_page/',views.login_page,name='login_page'),
    path('register_page/',views.register_page,name='register_page'),
    path('dashboard/<int:id>/',views.dashboard,name='dashboard'),
    path('phone_number_login/',views.phone_number_login,name='phone_number_login'),
    path('verifications/',views.verifications,name='verifications'),
    path('forget_password_page/',views.forget_password_page,name='forget_password_page'),
    path('signup_playlists/',views.signup_playlists,name='signup_playlists'),
]
