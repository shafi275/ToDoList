
from django.shortcuts import render
from django.conf import settings
from home.models import Task  # assuming you’ll be saving tasks later

def home(request):
    if request.method == "POST":
        taskName = request.POST.get('taskName')
        taskDesc = request.POST.get('taskDesc')
        print(taskDesc, taskName)
        ins=Task(tasktitle=taskName ,taskdesc= taskDesc )
        ins.save()
        
        # You can also save the task if needed:
        # Task.objects.create(name=taskName, description=taskDesc)
    return render(request, 'index.html')

from django.db.models import Q

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

