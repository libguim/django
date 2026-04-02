from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('create/', views.create_comment, name='create'),  # 댓글 등록
    path('<int:comment_id>/update/', views.update_comment, name='update'),  # 댓글 수정
    path('<int:comment_id>/delete/', views.delete_comment, name='delete'),
]