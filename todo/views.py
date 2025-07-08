from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm, RegisterForm
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'todo/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'todo/register.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        # Admin view
        users = User.objects.all()
        tasks = Task.objects.all()
        return render(request, 'todo/admin_dashboard.html', {
            'users': users,
            'tasks': tasks,
        })
    else:
        form = TaskForm()
        tasks = Task.objects.filter(user=request.user)

        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect('dashboard')

        return render(request, 'todo/user_dashboard.html', {
            'form': form,
            'tasks': tasks,
        })

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
from django.shortcuts import get_object_or_404
@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')

