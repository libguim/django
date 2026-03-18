from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from .models import Posts

from django.contrib import messages
from .form import PostCreateForm
from .form2 import PostUpdateForm

# 게시글 등록
# def create_post(request):
#     return HttpResponse('게시글 등록')

# 게시글 등록
def create_post(request):
    form = PostCreateForm()

    if request.method == 'POST':
        form = PostCreateForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, '게시글이 등록되었습니다.')
            return redirect("posts:read", post_id=post.id)
        else:
            messages.error(request, '게시글 등록에 실패했습니다.')

    return render(request, 'posts/create.html', {'form': form})

# 게시글 보기
# def get_post(request, post_id):
#     return HttpResponse('게시글 보기')

# 게시글 보기
def get_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    return render(request, 'posts/read.html', {'post': post})

# 게시글 수정
# def update_post(request, post_id):
#     return HttpResponse('게시글 수정')

# 게시글 수정
def update_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    form = PostUpdateForm(instance=post)

    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)

        if form.is_valid():
            # 입력한 비밀번호와 기존 비밀번호 비교
            if form.cleaned_data['password'] == post.password:
                post = form.save(commit=False)
                post.save()
                messages.success(request, '게시글이 수정되었습니다.')
                return redirect('posts:read', post_id=post.id)
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
        else:
            messages.error(request, '게시글 수정에 실패했습니다.')

    return render(request, 'posts/update.html', {'form': form})

# 게시글 삭제
# def delete_post(request, post_id):
#     return HttpResponse('게시글 삭제')

# 게시글 삭제 뷰 예시
def delete_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    
    if request.method == 'POST':
        # 모달의 input name="password" 값을 가져옴
        input_password = request.POST.get('password')
        
        if input_password == post.password:
            post.delete()
            messages.success(request, '게시글이 삭제되었습니다.')
            return redirect('posts:list')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('posts:read', post_id=post.id)
            
    return redirect('posts:read', post_id=post.id)

# 게시글 목록
# def get_posts(request):
#     return HttpResponse('게시글 목록')

# 게시글 목록
def get_posts(request):
    posts = Posts.objects.all().order_by('-created_at')
    return render(request, 'posts/list.html', {'posts': posts})