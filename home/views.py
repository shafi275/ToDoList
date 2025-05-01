
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from home.models import Task

# Home Page
def home(request):
    if request.method == "POST":
        taskName = request.POST.get('taskName')
        taskDesc = request.POST.get('taskDesc')
        ins = Task(tasktitle=taskName, taskdesc=taskDesc)
        ins.save()
    return render(request, 'index.html')


# Login Page (view only, does not authenticate yet)
def login(request):
    return render(request, 'login.html')


# Registration
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'register.html')


# Tasks with optional search
def tasks(request):
    query = request.GET.get('q')
    if query:
        alltasks = Task.objects.filter(
            Q(tasktitle__icontains=query) | Q(taskdesc__icontains=query)
        )
    else:
        alltasks = Task.objects.all()
    
    context = {'tasks': alltasks, 'query': query}
    return render(request, 'tasks.html', context)
