from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from accounts.models import Customer


# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

        messages.info(request, 'Login Failed PLease Try again')
        messages.info(request, 'Enter a valid username or password')

    return render(request, 'accounts/login.html')


def user_registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone_field')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exist')
                return redirect('user_registration')

            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exist')

                    return redirect('user_registration')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    data = Customer(user=user, phone=phone)
                    data.save()

                    our_user = authenticate(username=username, password=password)
                    if our_user is not None:
                        login(request, user)
                        return redirect('/')
        else:
            print('Error here ')
            messages.info(request, 'Password and confirm password mismatch')

            return redirect('user_registration')
    return render(request, 'accounts/register.html')


def user_logout(request):
    logout(request)
    return redirect('/')
