from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
def user_register(request):
    form=RegisterForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            login(request,user)
            messages.success(request,f"Your account created successfull.")
            return redirect('home')
    return render(request,'pages/register.html',{'form':form})
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        form=AuthenticationForm(request,request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    messages.success(request,f"You are now logged in as {username}.")
                    return redirect('home')
        messages.error(request,"Invalid username or password!")           
    return render(request,'pages/login.html')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")
