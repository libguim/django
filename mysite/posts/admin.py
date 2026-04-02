from django.contrib import admin
from .models import Posts
from comments.models import Comments

# 게시글을 조회할 때 해당 게시글에 달린 댓글도 함께 관리할 수 있도록 인라인으로 설정
class CommentsInline(admin.TabularInline):
    model = Comments
    extra = 1 # 추가 폼 개수

class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'updated_by', 'updated_at') # 관리자 페이지에서 게시글 목록에 표시할 필드 지정
    search_fields = ('title', 'created_by__username') # 관리자 페이지에서 게시글 검색 시 검색 대상 필드 지정
    list_filter = ('created_at',) # 관리자 페이지에서 게시글 목록에 필터 추가
    inlines = [CommentsInline] # 게시글 상세 페이지에서 댓글을 인라인으로 관리할 수 있도록 설정

admin.site.register(Posts, PostsAdmin) # 관리자 페이지에 Posts 모델 등록, PostsAdmin 클래스의 설정을 적용하여 게시글 관리 기능 제공