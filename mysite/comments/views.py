from django.shortcuts import render

# from django.http import HttpResponse
from django.http import JsonResponse
from django.utils import timezone

from posts.models import Posts
from .models import Comments

# 댓글 목록
# def get_comments(request):
#     return HttpResponse('댓글 목록')

# 댓글 목록
def get_comments(post_id):
    comments = Comments.objects.filter(post=post_id).order_by('-created_at')
    comment_list = []
    for comment in comments:
        comment_list.append({
            'id': comment.id,
            'post_id': comment.post.id,
            'content': comment.content,
            'created_by': comment.created_by.first_name,
            'updated_by': comment.updated_by.first_name,
            'created_at': comment.created_at
                            .astimezone(timezone.get_current_timezone())    
                            .strftime('%Y-%m-%d %H:%M'),
            'updated_at': comment.updated_at
                            .astimezone(timezone.get_current_timezone())
                            .strftime('%Y-%m-%d %H:%M'),
        })
    return comment_list

# 댓글 등록
# def create_comment(request):
#     return JsonResponse({'message': '댓글 등록'})    
def create_comment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'error', 'message': '로그인 후 이용해주세요.'})

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if not post_id:
            return JsonResponse({'result': 'error', 'message': '게시글을 선택해주세요.'})
        post = Posts.objects.get(id=post_id)
        if not post:
            return JsonResponse({'result': 'error', 'message': '게시글이 존재하지 않습니다.'})
        content = request.POST.get('content')
        if not content:
            return JsonResponse({'result': 'error', 'message': '댓글 내용을 입력해주세요.'})
        
        # 댓글 등록
        comment = Comments(
            post=post,
            content=content,
            created_by=request.user,
            updated_by=request.user
        )
        comment.save()

        # 댓글 목록
        comments = get_comments(post_id)
        return JsonResponse({'result': 'success', 'comments': comments, 'message': '댓글이 등록되었습니다.'})
    else:
        return JsonResponse({'message': '잘못된 요청입니다.'}, status=400)

# 댓글 수정
# def update_comment(request, comment_id):
#     return JsonResponse({'message': '댓글 수정'})

# 댓글 수정
def update_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'error', 'message': '로그인 후 이용해주세요.'})

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if not post_id:
            return JsonResponse({'result': 'error', 'message': '게시글을 선택해주세요.'})
        
        post = Posts.objects.get(id=post_id)
        if not post:
            return JsonResponse({'result': 'error', 'message': '게시글이 존재하지 않습니다.'})
        
        content = request.POST.get('content')
        if not content:
            return JsonResponse({'result': 'error', 'message': '댓글 내용을 입력해주세요.'})
        
        comment_id = request.POST.get('comment_id')
        if not comment_id:
            return JsonResponse({'result': 'error', 'message': '댓글을 선택해주세요.'})
        
        comment = Comments.objects.get(id=comment_id)
        if not comment:
            return JsonResponse({'result': 'error', 'message': '댓글이 존재하지 않습니다.'})
        
        if comment.created_by != request.user:
            return JsonResponse({'result': 'error', 'message': '댓글 수정 권한이 없습니다.'})

        # 댓글 수정
        comment.content = content
        comment.updated_by = request.user
        comment.save()

        # 댓글 목록
        comments = get_comments(post_id)
        
        return JsonResponse({'result': 'success', 'comments': comments, 'message': '댓글이 수정되었습니다.'})
    # else:
    #     return JsonResponse({'message': '잘못된 요청입니다.'}, status=400)

# 댓글 삭제
# def delete_comment(request, comment_id):
#     return JsonResponse({'message': '댓글 삭제'})

# 댓글 삭제
def delete_comment(request, comment_id):
    if not request.user.is_authenticated:
        return JsonResponse({'result': 'error', 'message': '로그인 후 이용해주세요.'})

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if not post_id:
            return JsonResponse({'result': 'error', 'message': '게시글을 선택해주세요.'})
        
        post = Posts.objects.get(id=post_id)
        if not post:
            return JsonResponse({'result': 'error', 'message': '게시글이 존재하지 않습니다.'})
        
        comment_id = request.POST.get('comment_id')
        if not comment_id:
            return JsonResponse({'result': 'error', 'message': '댓글을 선택해주세요.'})
        
        comment = Comments.objects.get(id=comment_id)
        if not comment:
            return JsonResponse({'result': 'error', 'message': '댓글이 존재하지 않습니다.'})
        
        if comment.created_by != request.user:
            return JsonResponse({'result': 'error', 'message': '댓글 삭제 권한이 없습니다.'})

        # 댓글 삭제
        comment.delete()

        # 댓글 목록
        comments = get_comments(post_id)
        
        return JsonResponse({'result': 'success', 'comments': comments, 'message': '댓글이 삭제되었습니다.'})
    else:
        return JsonResponse({'message': '잘못된 요청입니다.'}, status=400)