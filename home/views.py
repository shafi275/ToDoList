from django.shortcuts import render
from django.conf import settings



def home(request):
    return render(request, 'index.html')
def tasks(request):
    return render(request, 'tasks.html')
