from django.shortcuts import render,redirect,get_object_or_404
from .models import Task , Categories
from .forms import TaskForm , CategoryForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def task_list(request):

    status_filter = request.GET.get('status','all')
    category_filter = request.GET.get('category', 'all')

    task = Task.objects.filter(user = request.user)
    categories = Categories.objects.filter(user = request.user)

    if status_filter != 'all':
        task = task.filter(is_completed = (status_filter == 'completed'))

    if category_filter != 'all':
        task = task.filter(categories__id = category_filter)

    completed_tasks = task.filter(is_completed = True)
    pending_tasks = task.filter(is_completed = False)

    return render(request,'task_list.html',{
        'completed_tasks' : completed_tasks,
        'pending_tasks' : pending_tasks,
        'status_filter' : status_filter,
        'category_filter' : category_filter,
        'categories' : categories

    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(user = request.user, data = request.POST)
        if form.is_valid():
            form = form.save(commit=False) # commit = False mane form database e save hobena but model form ta create hobe jeta database e save howar jonne ready
            form.user = request.user
            form.save() #database e save hobe
            return redirect('task_list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'task_form.html', {'form' : form , 'title': 'Create Task'})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form = form.save(commit = False)
            form.user = request.user
            form.save()
            return redirect('task_list')
    else:
        form = CategoryForm()
    return render(request, 'task_form.html', {'form' : form , 'title' : 'Create Category'})

        


# Task detail page
@login_required
def task_detail(request,t_id):
    task = get_object_or_404(Task,id = t_id, user = request.user) 
    return render(request,'task_detail.html', {'task' : task})   

@login_required
def task_delete(request, t_id):
    task = get_object_or_404(Task, id = t_id, user = request.user)
    task.delete()
    return redirect('task_list')

# Mark task as completed
@login_required
def task_mark_completed(request, t_id):
    task = get_object_or_404(Task, id = t_id, user = request.user)
    task.is_completed = True
    task.save()
    return redirect('task_list')


#user register

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username , password = password)
            login(request,user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request,'register.html' ,{'form' : form })

