from django.shortcuts import render
from django.http import HttpResponse

# 회원가입
def register_account(request):
    return HttpResponse("회원가입 페이지입니다.")

# 로그인
def login_account(request):
    return HttpResponse("로그인 페이지입니다.")

# 로그아웃
def logout_account(request):          
    return HttpResponse("로그아웃 페이지입니다.")

# 프로필 보기
def get_profile(request):
    return HttpResponse("프로필 보기 페이지입니다.")

# 프로필 수정
def update_profile(request):
    return HttpResponse("프로필 수정 페이지입니다.")

# 비밀번호 수정
def update_password(request):
    return HttpResponse("비밀번호 수정 페이지입니다.")

# 아이디 찾기
def find_username(request):
    return HttpResponse("아이디 찾기 페이지입니다.")

# 비밀번호 초기화
def reset_password(request):
    return HttpResponse("비밀번호 초기화 페이지입니다.")

# 회원 탈퇴
def delete_account(request):
    return HttpResponse("회원 탈퇴 페이지입니다.")