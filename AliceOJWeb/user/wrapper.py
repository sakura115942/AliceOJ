from .forms import LoginForm

def login_require(fun):
    def wrapper(request, *args, **kwargs):
        if request.session['is_login']:
            return fun(request, *args, **kwargs)
        else:
            login_form = LoginForm()
            return render(request, 'login.html', locals())
    return wrapper
