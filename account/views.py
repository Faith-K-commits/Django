from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('account:home')
            else:
                return HttpResponse('Invalid username or password. Please try again later.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {
        'form': form
    })


@login_required
def home(request):
    return render(request, 'account/home.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('account:login')
