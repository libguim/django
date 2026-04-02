from django.urls import path
from . import views

app_name = 'users' # 네임스페이스 설정

urlpatterns = [
    path('', views.get_users, name='list'), # 사용자 목록 Read
    path('<int:user_id>/', views.get_user, name='read'), # 사용자 보기 Read
    path('<int:user_id>/delete/', views.delete_user, name='delete'), # 사용자
]