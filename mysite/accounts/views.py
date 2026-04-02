from django.http import HttpResponse

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import AccountDeleteForm, RegisterForm, LoginForm, ProfileUpdateForm, PasswordUpdateForm, UsernameFindForm, PasswordResetForm

import random
import string

# 회원가입
# def register_account(request):
#     return HttpResponse("회원가입 페이지입니다.")

# 회원가입
def register_account(request):
    if request.user.is_authenticated:
        return redirect('auth:profile')

    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
                first_name=form.cleaned_data["first_name"],
                email=form.cleaned_data["email"]
            )
            user.save()
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('auth:login')
        else:
            messages.error(request, '회원가입에 실패했습니다.')

    return render(request, 'accounts/register.html', 
                  {'form': form, 'message_class': 'col-4 mx-auto'})

# 로그인
# def login_account(request):
#     return HttpResponse("로그인 페이지입니다.")

# 로그인
def login_account(request):
    if request.user.is_authenticated:
        return redirect('auth:profile')

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            # 로그인 실패
            if user is None:
                messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
                return redirect('auth:login')
            
            # 로그인 성공
            login(request, user)
            return redirect('auth:profile')
        
        else:
            messages.error(request, '아이디 또는 비밀번호를 입력해주세요.')

    return render(request, 'accounts/login.html', 
                  {'form': form, 'message_class': 'col-4 mx-auto'})

# 로그아웃
# def logout_account(request):          
#     return HttpResponse("로그아웃 페이지입니다.")

# 로그아웃
def logout_account(request):
    logout(request)
    return redirect('auth:login')

# 프로필 보기
# def get_profile(request):
#     return HttpResponse("프로필 보기 페이지입니다.")

# 프로필 보기
@login_required(login_url='auth:login')
def get_profile(request):
    return render(request, 'accounts/profile.html', {'message_class': 'col-4 mx-auto'})

# 프로필 수정
# def update_profile(request):
#     return HttpResponse("프로필 수정 페이지입니다.")

# 프로필 수정
@login_required(login_url='auth:login')
def update_profile(request):
    form = ProfileUpdateForm(instance=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # 세션 갱신
            messages.success(request, '프로필 수정이 완료되었습니다.')
            return redirect('auth:profile')
        else:
            messages.error(request, '프로필 수정에 실패했습니다.')

    return render(request, 'accounts/update_profile.html', 
                  {'form': form, 'message_class': 'col-4 mx-auto'})

# 비밀번호 수정
# def update_password(request):
#     return HttpResponse("비밀번호 수정 페이지입니다.")

# 비밀번호 수정
@login_required(login_url='auth:login')
def update_password(request):
    form = PasswordUpdateForm()

    if request.method == 'POST':
        form = PasswordUpdateForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            password1 = form.cleaned_data["password1"]

            user = authenticate(request, username=request.user.username, password=password)
            if user is None:
                messages.error(request, '현재 비밀번호가 올바르지 않습니다.')
                return redirect('auth:update_password')
            
            user = request.user
            user.set_password(password1)
            user.save() 

            logout(request)
            messages.success(request, '비밀번호 수정이 완료되었습니다.')
            return redirect('auth:login')
        else:
            messages.error(request, '비밀번호 수정에 실패했습니다.')

    return render(request, 'accounts/update_password.html', 
                  {'form': form, 'message_class': 'col-4 mx-auto'})

# 아이디 찾기
# def find_username(request):
#     return HttpResponse("아이디 찾기 페이지입니다.")

# 아이디 찾기
def find_username(request):
    if request.user.is_authenticated:
        return redirect('auth:profile')
    
    form = UsernameFindForm()

    if request.method == 'POST':
        form = UsernameFindForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            email = form.cleaned_data["email"]
            user = User.objects.filter(first_name=first_name, email=email).first()
            if user:
                messages.success(request, f'아이디는 {user.username}입니다.')
                return redirect('auth:login')
            else:
                messages.error(request, '아이디 찾기에 실패했습니다.')
        else:
            messages.error(request, '아이디 찾기에 실패했습니다.')

    return render(request, 'accounts/find_username.html', 
                  {'form': form, 'message_class': 'col-4 mx-auto'})

# 비밀번호 초기화
# def reset_password(request):
#     return HttpResponse("비밀번호 초기화 페이지입니다.")

# 비밀번호 초기화
def reset_password(request):
    if request.user.is_authenticated:
        return redirect('auth:profile')
    
    form = PasswordResetForm()

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            user = User.objects.filter(first_name=first_name,username=username, email=email).first()
            if user:
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                user.set_password(password)
                user.save()

                messages.success(request, f'비밀번호가 초기화되었습니다. 새로운 비밀번호는 {password}입니다.')
                return redirect('auth:login')
            else:
                messages.error(request, '비밀번호 초기화에 실패했습니다.')

    return render(request, 'accounts/reset_password.html', 
                  {'form': form, 'message_class': 'col-4 mx-auto'})

# 회원 탈퇴
# def delete_account(request):
#     return HttpResponse("회원 탈퇴 페이지입니다.")

# 회원 탈퇴
@login_required(login_url='auth:login')
def delete_account(request):
    form = AccountDeleteForm()

    if request.method == 'POST':
        form = AccountDeleteForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.filter(first_name=first_name, username=username, email=email).first()
            authenticated = authenticate(request, username=username, password=password)

            if user and authenticated is not None:
                user.delete()
                logout(request)
                messages.error(request, '회원 탈퇴가 완료되었습니다.')
                return redirect('auth:login')
            else:
                messages.error(request, '회원 탈퇴에 실패했습니다. 입력정보를 확인하세요.')

    return render(request, 'accounts/delete_account.html', 
                  {'form': form, 'message_class': 'col-4 mx-auto'})