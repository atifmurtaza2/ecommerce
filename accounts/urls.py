
from django.urls import path,include
from accounts import views
urlpatterns = [

    path('user_login',views.user_login,name='user_login'),
    path('user_register', views.user_registration, name='user_registration'),
    path('user_logout', views.user_logout, name='user_logout'),

]