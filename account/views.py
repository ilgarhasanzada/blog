from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User=get_user_model()
def user_register(request):
    form = RegisterForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.save()
            login(request, user)
            messages.success(request, "Your account created successfull.")
            return redirect('home')
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        try:
            username = request.POST['username']
            password = request.POST['password']
            username_for_email = User.objects.get(email = username).username
            user = authenticate(request,username = username_for_email,password = password)
            if user:
                    if user.is_active:
                        login(request,user)
                        messages.success(request,f"You are now logged in as {username_for_email}.")
                        return redirect('home')
        except:
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request,username = username,password = password)
                if user:
                    if user.is_active:
                        login(request,user)
                        messages.success(request,f"You are now logged in as {username}.")
                        return redirect('home')
        messages.error(request, "Invalid username or password!")
    form= AuthenticationForm()  
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")
    return redirect('login')