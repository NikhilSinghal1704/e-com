from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name = "SignUp"),
    path('profile/', views.profile_details, name='profile_details'),
    path('signin', views.signin, name = "SignIn"),
    path('signout', views.signout, name = "logout"),
    path('activate/<uidb64>/<token>/', views.activate, name = "Activate"),
]