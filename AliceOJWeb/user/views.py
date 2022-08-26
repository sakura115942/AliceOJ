from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import User, UserData
from .forms import (LoginForm, RegisterForm, )
# Create your views here.


@csrf_exempt
def login(request):
    print(request.POST)
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/home/')

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        message = 'please check your form'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = User.objects.get(username=username)
            except:
                message = 'user does not exist'
                return render(request, 'login.html', locals())

            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return redirect('/home/')
            else:
                message = 'password error'
                return render(request, 'login.html', locals())
        else:
            print(login_form.errors.as_data())
            return render(request, 'login.html', locals())

    login_form = LoginForm()
    return render(request, 'login.html', locals())


@csrf_exempt
def register(request):

    if request.session.get('is_login', None):
        return redirect('/home/')
    
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        
        if register_form.is_valid():
            
            # email = register_form.cleaned_data.get('email')
            
            # same_user_name = User.objects.filter(username=username)
            # if same_user_name:
            #     message = 'username already exist'
            #     return render(request, 'register.html', locals())
            
            # same_user_email = User.objects.filter(email=email)
            # if same_user_email:
            #     message = 'the email address is already registered'
            #     return render(request, 'register.html', locals())

            register_form.save()
            username = register_form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            user_data = UserData()
            user_data.user = user
            user_data.save()
            message = 'register successfully'
            login_form = LoginForm()
            return render(request, 'login.html', locals())
        else:
            return render(request, 'register.html', locals())
    register_form = RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return redirect("/home/")

def center(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    return render(request, 'center.html', locals())

def rank(request):
    menu = 'rank'
    user_data = UserData.objects.order_by('-score')[:10]
    return render(request, 'rank.html', locals())
