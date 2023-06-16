from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, TaskForm, TaskFilterForm
from .models import Category, Task

# Categories ----------------------------------------------------------------s


@login_required(login_url="/login")
def add_category(request):
    template_name = 'tasks/categories/add_category.html'
    if request.method == 'POST':
        form = CategoryForm(request.user, request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()
            messages.success(request, 'Categoria adicionada com sucesso')
            return redirect('tasks:add_category')
    else:
        form = CategoryForm(request.user)
        return render(request, template_name, context={'form': form})


@login_required(login_url="/login")
def edit_category(request, id_category):
    template_name = 'tasks/categories/edit_category.html'
    category = Category.objects.get(id=id_category, owner=request.user)
    context = {}
    if request.method == 'POST':
        form = CategoryForm(request.POST or None,
                            instance=category, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('tasks:list_categories')
    form = CategoryForm(instance=category, user=request.user)
    context = {
        'form': form
    }
    return render(request, template_name, context)


@login_required(login_url="/login")
def list_categories(request):
    template_name = 'tasks/categories/list_categories.html'
    categories = Category.objects.filter(owner=request.user)
    context = {'categories': categories}
    return render(request, template_name, context)


@login_required(login_url="/login")
def delete_category(request, id_category):
    category = Category.objects.get(pk=id_category, owner=request.user)
    if category.owner == request.user:
        category.delete()
    else:
        messages.error(
            request, 'Você não tem permissão para excluir esta categoria.')
        return (redirect('tasks:list_categories'))
    return (redirect('tasks:list_categories'))


# Task ---------------------------------------------------------------------

@login_required(login_url="/login")
def add_task(request):
    context = {}
    template_name = 'tasks/tasks/add_task.html'
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()
            form.save_m2m()
            messages.success(request, 'Tarefa adicionada com sucesso.')
    form = TaskForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url="/login")
def edit_task(request, id_task):
    template_name = 'tasks/tasks/edit_task.html'
    task = get_object_or_404(Task, id=id_task, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:list_tasks')
    else:
        form = TaskForm(request.user, instance=task)
    context = {
        'task': task,
        'form': form
    }
    return render(request, template_name, context)


@login_required(login_url="/login")
def list_tasks(request):
    template_name = 'tasks/tasks/list_tasks.html'
    tasks = Task.objects.filter(owner=request.user)
    context = {
        'tasks': tasks
    }
    return render(request, template_name, context)


@login_required(login_url="/login")
def delete_task(request, id_task):
    task = Task.objects.get(id=id_task)
    if task.owner == request.user:
        task.delete()
    else:
        messages.error(
            request, 'Você não tem permissão para excluir esta tarefa.')
        return (redirect('core:home'))
    return (redirect('tasks:list_tasks'))


@login_required(login_url="/login")
def complete_task(request, id_task):
    task = Task.objects.get(id=id_task)
    if task.owner == request.user:
        task.completed = True
        task.save()
    else:
        messages.error(
            request, 'Você não tem permissão para excluir esta tarefa.')
        return (redirect('core:home'))
    return (redirect('tasks:list_tasks'))


@login_required(login_url="/login")
def not_complete_task(request, id_task):
    task = Task.objects.get(id=id_task)
    if task.owner == request.user:
        task.completed = False
        task.save()
    else:
        messages.error(
            request, 'Você não tem permissão para excluir esta tarefa.')
        return (redirect('core:home'))
    return (redirect('tasks:list_tasks'))


@login_required(login_url="/login")
def show_completed_tasks(request):
    completed_tasks = Task.objects.filter(completed=True)
    context = {
        'tasks': completed_tasks
    }
    return render(request, 'tasks/tasks/completed_tasks.html', context)


@login_required(login_url="/login")
def low_priority_tasks(request):
    tasks = Task.objects.filter(priority='B')
    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/tasks/low_priority_tasks.html', context)


@login_required(login_url="/login")
def medium_priority_tasks(request):
    tasks = Task.objects.filter(priority='M')
    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/tasks/medium_priority_tasks.html', context)


@login_required(login_url="/login")
def high_priority_tasks(request):
    tasks = Task.objects.filter(priority='A')
    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/tasks/high_priority_tasks.html', context)


@login_required(login_url="/login")
def imcomplete_tasks(request):
    tasks = Task.objects.filter(completed=False)
    context = {
        'tasks': tasks
    }
    return render(request, 'tasks/tasks/imcomplete_tasks.html', context)


@login_required(login_url="/login")
def show_task(request, id_task):
    task = Task.objects.get(id=id_task)
    context = {
        'task': task,
    }
    return render(request, 'tasks/tasks/show_task.html', context)


def task_filter(request):
    form = TaskFilterForm(request.GET)
    tarefis = Task.objects.all()

    if form.is_valid():
        name = form.cleaned_data['name']
        status = form.cleaned_data['status']
        priority = form.cleaned_data['priority']
        category = form.cleaned_data['category']
        completed = form.cleaned_data['completed']
        end_date = form.cleaned_data['end_date']

        if name:
            tarefis = tarefis.filter(name__icontains=name)
        if status:
            tarefis = tarefis.filter(status=status)
        if priority:
            tarefis = tarefis.filter(priority=priority)
        if category:
            tarefis = tarefis.filter(category=category)
        if completed is not None:
            tarefis = tarefis.filter(completed=completed)
        if end_date is not None:
            tarefis = tarefis.filter(end_date=end_date)

    context = {
        'form': form,
        'tarefis': tarefis,
    }
    return render(request, 'tasks/tasks/list_task.html', context)