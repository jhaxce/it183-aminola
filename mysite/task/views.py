from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm
from django.contrib import messages  # For adding messages to be displayed
from rest_framework.authtoken.models import Token
# from django.views.decorators.csrf import csrf_exempt
import json

# Home Page
def home(request):
    if request.user.is_authenticated:
        return redirect("task_list")  # Redirect to task list if logged in
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If user is authenticated, log them in and redirect to the next URL
            login(request, user)
            next_url = request.GET.get('next', 'task_list')  # Redirect after login
            return redirect(next_url)
        else:
            # If authentication fails, show an error message
            messages.error(request, "Username or password is incorrect or does not exist")

    return render(request, "public/home.html")
    
# About Page
def about(request):
    return render(request, "public/about.html")

# Privacy Policy Page
def privacy(request):
    return render(request, "public/privacy.html")

# Terms of Service Page
def tos(request):
    return render(request, "public/tos.html")
    
# Cookie Policy Page
def cookie(request):
    return render(request, "public/cookie.html")

# Sign Up
def signup(request):
    if request.user.is_authenticated:
        return redirect("task_list")  # Redirect to task list if logged in

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task_list")
    else:
        form = UserCreationForm()
    return render(request, "account/signup.html", {"form": form})

# Login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('task_list')  # Redirect to task list if the user is already logged in

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If user is authenticated, log them in and redirect to the next URL
            login(request, user)
            next_url = request.GET.get('next', 'task_list')  # Redirect after login
            return redirect(next_url)
        else:
            # If authentication fails, show an error message
            messages.error(request, "Username or password is incorrect or does not exist")
    
    # return render(request, "account/login.html")
    return redirect("home")

# Logout
def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
def account_view(request):
    """Renders the account settings page."""
    # Get or create the token for the user
    token, created = Token.objects.get_or_create(user=request.user)
    return render(request, 'account/account.html', {'token': token.key})

@login_required
def update_username(request):
    """Handles username update."""
    if request.method == 'POST':
        new_username = request.POST.get('username')
        if new_username:
            try:
                request.user.username = new_username
                request.user.save()
                messages.success(request, 'Username updated successfully!')
                return redirect('account')
            except Exception as e:
                messages.error(request, f'Error updating username: {e}')
        else:
            messages.error(request, 'Username cannot be empty.')
    return redirect('account')

@login_required
def update_password(request):
    """Handles password update."""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Incorrect current password.')
            return redirect('account')
        
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('account')
        
        try:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep the user logged in after password change
            messages.success(request, 'Password updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating password: {e}')
    return redirect('account')

@login_required
def regenerate_token(request):
    """Handles token regeneration."""
    if request.method == 'POST':
        try:
            token, created = Token.objects.get_or_create(user=request.user)
            token.delete()  # Delete the old token
            new_token = Token.objects.create(user=request.user)  # Create a new token
            messages.success(request, 'Access token regenerated successfully!')
            return redirect('account')
        except Exception as e:
            messages.error(request, f'Error regenerating token: {e}')
    return redirect('account')

# Task List
@login_required
def task_list(request):
    # Filter tasks by user and categorize by 'is_priority' and 'is_done' status
    priority_tasks = Task.objects.filter(user=request.user, is_priority=True, is_done=False).order_by('-timestamp')
    task_tasks = Task.objects.filter(user=request.user, is_priority=False, is_done=False).order_by('-timestamp')
    completed_tasks = Task.objects.filter(user=request.user, is_done=True).order_by('-timestamp')

    # Get counts for each category
    priority_count = priority_tasks.count()
    task_count = task_tasks.count()
    completed_count = completed_tasks.count()

    # Pass the tasks and counts to the template
    return render(
        request,
        "task/task_list.html",
        {
            "priority_tasks": priority_tasks,
            "task_tasks": task_tasks,
            "completed_tasks": completed_tasks,
            "priority_count": priority_count,
            "task_count": task_count,
            "completed_count": completed_count,
        },
    )

@login_required
def update_task(request, task_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.get(id=task_id)

        if 'is_done' in data:
            task.is_done = data['is_done']
        if 'is_priority' in data:
            task.is_priority = data['is_priority']

        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

# Add/Edit Task
@login_required
def task_form(request, task_id=None):
    task = get_object_or_404(Task, id=task_id) if task_id else None
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user  # Assign the current logged-in user to the task
            new_task.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "task/task_form.html", {"form": form, "task": task})

# Delete Task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect("task_list")

@login_required
def delete_completed_tasks(request):
    if request.method == 'POST':
        # Delete all completed tasks for the current user
        completed_tasks = Task.objects.filter(is_done=True, user=request.user)
        completed_tasks.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)