from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from .forms import SignUpForm, LogInForm, UpdateForm
from django.contrib.auth.decorators import login_required
from account_manager.models import Account

# Create your views here.


# def home(request):
#     total_users = Account.objects.count()
#     return render(request, 'home.html', {'total': total_users})


def signup(request):
    context = {}
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            print(email, 'is Successfully registered')
            account = authenticate(email=email, password=raw_password)
            auth_login(request, account)
            return redirect('ebook_posts')
        else:
            context['form'] = form
    else:
        form = SignUpForm()
        context['form'] = form
    return render(request, 'registration/signup.html', context)


def login(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('ebook_posts')
    if request.POST:
        form = LogInForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                auth_login(request, user)
                return redirect('ebook_posts')
    else:
        form = LogInForm()
    context['form'] = form
    return render(request, 'registration/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('ebook_posts')


def update(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    if request.POST:
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UpdateForm(
            initial={
                'email': request.user.email,
                'username': request.user.username,
            }
        )
    context['form'] = form
    return render(request, 'registration/update.html', context)
