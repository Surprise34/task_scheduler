from django.shortcuts import render, render_to_response, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from .forms import TaskForm
from django.http import HttpResponse, Http404
from threading import Timer

# Create your views here.

def tasks_list(request):
    if request.user.is_authenticated:
        tasks_list = Task.objects.filter(author=request.user).order_by('created_date')
        return render(
            request, 'index.html', {
                'tasks':tasks_list,
            }
        )
    else:
        return render(request, 'index.html')

@login_required
def task_detail(request , task_id):
    try:
        task = Task.objects.select_related('author').get(id=task_id)
    except Task.DoesNotExist:
        raise Http404
    if request.user != task.author:
        raise Http404
    time_left = int((timezone.now()-task.created_date).total_seconds())
    speed = int(task.duration.total_seconds()*10)
    per = int(time_left/task.duration.total_seconds()*100)
    return render(
        request, 'task_detail.html',{
            'task':task,
            'speed':speed,
            'per':per,
        }
    )

def task_execute(task_id):
    task = Task.objects.get(id=task_id)
    task.is_done=True
    task.save()

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            timer = Timer(task.duration.total_seconds(),task_execute,args=(task.id,))
            timer.start()
            return redirect(tasks_list)
    else:
        form = TaskForm()
    return render (
        request, 'task_create.html', {
            'form' : form,
        }
    )



            
            
        
            
            
            
            








    
