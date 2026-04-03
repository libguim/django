from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('register/', views.register_account, name='register'),
    path('login/', views.login_account, name='login'),
    path('logout/', views.logout_account, name='logout'),
    path('profile/', views.get_profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-password/', views.update_password, name='update_password'),
    path('find-username/', views.find_username, name='find_username'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
]