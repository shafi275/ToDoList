
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from home.models import Task
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Home Page
@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        taskName = request.POST.get('taskName')
        taskDesc = request.POST.get('taskDesc')
        ins = Task(tasktitle=taskName, taskdesc=taskDesc, user=request.user)
        ins.save()
    return render(request, 'index.html')


# Login Page (view only, does not authenticate yet)
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')  # or wherever you want
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

#logout
def logout_view(request):
    logout(request)
    return redirect('login')
# Registration
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email    = request.POST['email']
        password = request.POST['password1']  # match form field
        confirm  = request.POST['password2']  # match form field

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')
    return render(request, 'register.html')



# Tasks with optional search
@login_required(login_url='login')
def tasks(request):
    query = request.GET.get('q')
    if query:
        # Filter tasks by the logged-in user and search query
        alltasks = Task.objects.filter(
            Q(tasktitle__icontains=query) | Q(taskdesc__icontains=query),
            user=request.user  # Filter tasks by the logged-in user
        )
    else:
        # Only show tasks for the logged-in user
        alltasks = Task.objects.filter(user=request.user)  # Filter tasks by user
    
    context = {'tasks': alltasks, 'query': query}
    return render(request, 'tasks.html', context)
