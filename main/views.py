from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
    tasks = Task.objects.filter(done=False, user=request.user)
    return render(request, 'main/task_list.html', {'tasks': tasks})


@login_required
def task_detail(request, task_slug):
    task = get_object_or_404(Task, slug__iexact=task_slug, user=request.user)
    return render(request, 'main/task_detail.html', {'task': task})


@login_required
def done_task_list(request):
    tasks = Task.objects.filter(done=True, user=request.user)
    return render(request, 'main/done_task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if(form.is_valid()):
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect(new_task)

    return render(request, 'main/task_create.html', {'form': form})


@login_required
def task_update(request, task_slug):
    task = get_object_or_404(Task, slug__iexact=task_slug, user=request.user)
    form = TaskForm(request.POST or None, instance=task)

    if request.method == 'POST':
        if(form.is_valid()):
            form.save()
            return redirect(task)

    return render(request, 'main/task_update.html', {'form': form})


@login_required
def task_delete(request, task_slug):
    task = get_object_or_404(Task, slug__iexact=task_slug, user=request.user)
    task.delete()
    return redirect('main:task_list')


@login_required
def task_do(request, task_slug):
    task = get_object_or_404(Task, slug__iexact=task_slug, user=request.user)
    task.done = True
    task.finished_on = timezone.now()
    task.save()
    return redirect(task)


@login_required
def task_undo(request, task_slug):
    task = get_object_or_404(Task, slug__iexact=task_slug, user=request.user)
    task.done = False
    task.finished_on = None
    task.save()
    return redirect(task)
