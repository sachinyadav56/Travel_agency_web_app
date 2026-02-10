from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    # 👇 get redirect URL (VERY IMPORTANT)
    next_url = request.GET.get('next')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 redirect back to booking page
            if next_url:
                return redirect(next_url)

            return redirect('home')

        messages.error(request, "Invalid username or password")

    # 👇 send next to template
    return render(request, 'login.html', {'next': next_url})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    return render(request, "profile.html")
