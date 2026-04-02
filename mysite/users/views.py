from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

# 사용자 목록
@login_required(login_url='auth:login')
@user_passes_test(lambda u: u.is_superuser)
def get_users(request):
    return HttpResponse("사용자 목록 페이지입니다.")

# 사용자 보기
@login_required(login_url='auth:login')
@user_passes_test(lambda u: u.is_superuser)
def get_user(request, user_id):
    return HttpResponse(f"사용자 보기입니다.")

# 사용자 삭제
@login_required(login_url='auth:login')
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    return HttpResponse(f"사용자 삭제입니다.")
