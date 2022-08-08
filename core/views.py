from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

from django.views import View
from django.http import HttpResponse
from django.utils.html import mark_safe

# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging

FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)


# log.setLevel(logging.INFO)


class Index(View):
    def get(self, request, *args, **kwargs):
        log.debug("Index Start")

        context = {'rows': 'rows'}
        return render(request, 'core/index.html', context)

    def post(self, request, *args, **kwargs):
        return HttpResponse(None)


# 회원 가입
class Signup(View):
    def get(self, request, *args, **kwargs):
        # signup으로 GET 요청이 왔을 때, 회원가입 화면을 띄워준다.
        return render(request, 'core/signup.html')

    def post(self, request, *args, **kwargs):
        # password와 confirm에 입력된 값이 같다면
        if request.POST['password'] == request.POST['confirm']:
            # user 객체를 새로 생성
            user = User.objects.create_user(username=request.POST['username'],
                                            password=request.POST['password'])
            # 로그인 한다
            auth.login(request, user)
            return redirect('/')
        return HttpResponse(None)


# 로그인
class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/login.html')

    def post(self, request, *args, **kwargs):
        # login.html에서 넘어온 username과 password를 각 변수에 저장한다.
        username = request.POST['username']
        password = request.POST['password']

        # 해당 username과 password와 일치하는 user 객체를 가져온다.
        user = auth.authenticate(request, username=username, password=password)

        # 해당 user 객체가 존재한다면
        if user is not None:
            # 로그인 한다
            auth.login(request, user)
            return redirect('/admin/')
        # 존재하지 않는다면
        else:
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
            return render(request, 'core/login.html',
                          {'error': 'username or password is incorrect.'})


# 로그 아웃
class Logout(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/login.html')

    def post(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('/')

