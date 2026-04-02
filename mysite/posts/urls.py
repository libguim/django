from django.urls import path
from . import views

app_name = 'posts' # 네임스페이스 설정

urlpatterns = [
    path('create/', views.create_post, name='create'), # 게시글 등록 Create
    path('<int:post_id>/', views.get_post, name='read'), # 게시글 상세 조회 Read
    path('<int:post_id>/update/', views.update_post, name='update'), # 게시글 수정 Update
    path('<int:post_id>/delete/', views.delete_post, name='delete'), # 게시글 삭제 Delete
    path('', views.get_posts, name='list'), # 게시글 목록 Read
    path('<int:post_id>/download/', views.download_file, name='download'), # 첨부 파일 다운로드
]
