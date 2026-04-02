import os # 파일 업로드 시 파일 경로 처리를 위한 os 라이브러리 임포트
import uuid # 파일 업로드 시 고유한 파일명을 생성하기 위한 uuid 라이브러리 임포트
from mysite import settings # settings 임포트

from urllib.parse import quote # 파일 다운로드 시 한글 파일명 처리를 위한 quote 함수 임포트
from django.http import HttpResponse # HttpResponse 임포트

from django.shortcuts import render, redirect, get_object_or_404 # get_object_or_404 임포트
from django.contrib import messages # 메시지 프레임워크 임포트
from django.core.paginator import Paginator # 페이지네이션을 위한 Paginator 클래스 임포트
from django.db.models import Q # 검색 기능을 위한 Q 객체 임포트
from django.contrib.auth.hashers import make_password, check_password # 비밀번호 해싱과 검증을 위한 함수 임포트

from django.contrib.auth.decorators import login_required # 로그인 필요 데코레이터 임포트

from .models import Posts
from .form import PostCreateForm
from .form2 import PostUpdateForm

from comments.models import Comments

# 게시글 등록
# def create_post(request):
#     return HttpResponse('게시글 등록')

# 게시글 등록
@login_required(login_url='auth:login')
def create_post(request):
    form = PostCreateForm() # 게시글 등록 폼 객체 생성

    if request.method == 'POST': # POST 요청이 들어오면 폼 객체에 요청 데이터를 바인딩
        form = PostCreateForm(request.POST) # 폼 객체에 POST 데이터 바인딩

        if form.is_valid():
            post = form.save(commit=False)
            # post.password = make_password(form.cleaned_data['password'])
            post.created_by = request.user
            post.updated_by = request.user
            post.save()

            # 파일 업로드
            if request.FILES.get('uploadFile'):
                filename = uuid.uuid4().hex # 고유한 파일명 생성
                file = request.FILES.get('uploadFile')

                # 파일 저장 경로
                file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(filename))
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))

                # 파일 저장
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

                post.filename = filename
                post.original_filename = file.name
                post.save()

            messages.success(request, '게시글이 등록되었습니다.')
            return redirect("posts:read", post_id=post.id)
        else:
            messages.error(request, '게시글 등록에 실패했습니다.')

    return render(request, 'posts/create.html', {'form': form}) # 게시글 등록 폼을 템플릿으로 전달

# 게시글 보기
# def get_post(request, post_id):
#     return HttpResponse('게시글 보기')

# 게시글 보기
@login_required(login_url='auth:login')
def get_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    # return render(request, 'posts/read.html', {'post': post})
    comments = Comments.objects.filter(post=post_id).order_by('-created_at')
    return render(request, 'posts/read.html', {'post': post, 'comments': comments})

# 게시글 수정
# def update_post(request, post_id):
#     return HttpResponse('게시글 수정')

# 게시글 수정
@login_required(login_url='auth:login')
def update_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)

    if post.created_by != request.user:
        messages.error(request, '게시글 수정 권한이 없습니다.')
        return redirect('posts:read', post_id=post.id)
    # post_password = post.password
    form = PostUpdateForm(instance=post) # 게시글 수정 폼 객체 생성, instance 매개변수로 기존 게시글 데이터를 전달하여 폼 초기화

    if request.method == 'POST':
        # form = PostUpdateForm(request.POST)
        form = PostUpdateForm(request.POST, instance=post) # 폼 객체에 POST 데이터와 기존 게시글 데이터를 바인딩하여 폼 초기화

        if form.is_valid():
            # if check_password(form.cleaned_data['password'], post_password):
            #     post = form.save(commit=False)
            #     post.password = make_password(form.cleaned_data['password'])
            #     post.save()

                post.title = form.cleaned_data['title']
                post.content = form.cleaned_data['content']
                post.updated_by = request.user
                post.save()

                # 파일 삭제 로직
                # if form.cleaned_data['deleteFile']:
                # if form.cleaned_data.get('deleteFile'):
                if request.POST.get('deleteFile'):
                    if post.filename:
                        # 실제 파일 삭제
                        file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(post.filename))
                        if os.path.exists(file_path):
                            os.remove(file_path)

                        post.filename = None
                        post.original_filename = None
                        post.save()

                # 파일 업로드 로직
                if request.FILES.get('uploadFile'):
                    # 기존 파일이 있다면 삭제 후 교체
                    if post.filename:
                        file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(post.filename))
                        if os.path.exists(file_path):
                            os.remove(file_path)

                    filename = uuid.uuid4().hex
                    file = request.FILES['uploadFile']

                    # 파일 저장 경로 설정
                    file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(filename))
                    if not os.path.exists(os.path.dirname(file_path)):
                        os.makedirs(os.path.dirname(file_path))

                    # 파일 저장
                    with open(file_path, 'wb') as f:
                        for chunk in file.chunks():
                            f.write(chunk)

                    post.filename = filename
                    post.original_filename = file.name
                    post.save()

                messages.success(request, '게시글이 수정되었습니다.')
                return redirect('posts:read', post_id=post.id)
            # else:
            #     messages.error(request, '비밀번호가 일치하지 않습니다.')
        else:
            messages.error(request, '게시글 수정에 실패했습니다.')
    else:
        form = PostUpdateForm(instance=post)

    return render(request, 'posts/update.html', {'form': form})

# 게시글 삭제
# def delete_post(request, post_id):
#     return HttpResponse('게시글 삭제')

# 게시글 삭제
@login_required(login_url='auth:login')
def delete_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    # password = request.POST.get('password')

    if post.created_by != request.user:
        messages.error(request, '게시글 삭제 권한이 없습니다.')
        return redirect('posts:read', post_id=post.id)
    
    if request.method == 'POST':
        # if check_password(password, post.password):
            # 파일 삭제
            if post.filename:
                file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(post.filename))
                if os.path.exists(file_path):
                    os.remove(file_path)

            post.delete()
            messages.success(request, '게시글이 삭제되었습니다.')
            return redirect('posts:list')
        # else:
        #     messages.error(request, '비밀번호가 일치하지 않습니다.')
        #     return redirect('posts:read', post_id=post.id)

# 게시글 목록
# def get_posts(request):
#     return HttpResponse('게시글 목록')

# 게시글 목록
@login_required(login_url='auth:login')
def get_posts(request):
    page = request.GET.get('page', 1) 
    posts = Posts.objects.all().order_by('-created_at') # 최신 게시글이 먼저 보이도록 정렬

    searchType = request.GET.get('searchType')
    searchKeyword = request.GET.get('searchKeyword')

    # 검색 조건 처리
    if searchType not in [None, ''] and searchKeyword not in [None, '']:
        if searchType == 'all':
            # 검색어가 제목, 내용, 작성자(username) 중 하나라도 포함된 게시글 필터링
            posts = posts.filter( 
                Q(title__contains=searchKeyword) | 
                Q(content__contains=searchKeyword) | 
                Q(username__contains=searchKeyword)
            )
        elif searchType == 'title':
            posts = posts.filter(
                Q(title__contains=searchKeyword)
            )
        elif searchType == 'content':
            posts = posts.filter(
                Q(content__contains=searchKeyword)
            )
        # elif searchType == 'username':
        #     posts = posts.filter(
        #         Q(username__contains=searchKeyword)
        #     )
        elif searchType == 'full_name':
            posts = posts.filter(
                Q(create_by__first_name__contains=searchKeyword)
            )        

    # 페이지네이션 - Paginator 라이브러리 사용
    paginator = Paginator(posts, 10)  # 페이지당 10개 게시글
    page_obj = paginator.get_page(page)

    # 현재 페이지의 첫번째 게시글 번호 계산
    start_index = paginator.count - (paginator.per_page * (page_obj.number - 1))

    # 순번 계산하여 게시글 리스트에 추가
    for index, _ in enumerate(page_obj, start=0):
        page_obj[index].index_number = start_index - index

    # 페이지 객체와 검색 조건을 템플릿으로 전달
    return render(request, 'posts/list.html', {
        'posts': page_obj,
        'searchType': searchType,
        'searchKeyword': searchKeyword
    })

# 첨부 파일 다운로드
@login_required(login_url='auth:login')
def download_file(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(post.filename))

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            encoded_filename = quote(post.original_filename)
            response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'
            return response

    return HttpResponse(status=404)