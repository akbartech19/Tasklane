from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Task, Profile
from django.contrib.auth import logout, update_session_auth_hash
from django.conf import settings


@login_required
def home_page(request):
    all_tasks = Task.objects.filter(user=request.user)
    open_count = all_tasks.filter(status=False).count()
    done_count = all_tasks.filter(status=True).count()

    tasks = all_tasks.order_by("-created_at")

    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")
    q = request.GET.get("q", "").strip()

    if status == "open":
        tasks = tasks.filter(status=False)
    elif status == "done":
        tasks = tasks.filter(status=True)

    if priority in ("low", "medium", "high"):
        tasks = tasks.filter(priority=priority)

    if q:
        tasks = tasks.filter(title__icontains=q)

    return render(request, "index.html", {
        "tasks": tasks,
        "status": status,
        "priority": priority,
        "q": q,
        "open_count": open_count,
        "done_count": done_count,
    })


@login_required
def task_mng(request):
    if request.method == "POST":
        Task.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description", ""),
            priority=request.POST.get("priority", "medium"),
            due_date=request.POST.get("due_date") or None,
            user=request.user,
        )
        messages.success(request, "Task is created successfully !")
        return redirect("task:manage")

    tasks = Task.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "manage.html", {"tasks": tasks})


@login_required
@require_POST
def toggle_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = not task.status
    task.save()

    next_url = request.POST.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
        return redirect(next_url)
    return redirect("task:home")


@login_required
@require_POST
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.title = request.POST.get("title", task.title)
    task.description = request.POST.get("description", "")
    task.priority = request.POST.get("priority", task.priority)
    task.due_date = request.POST.get("due_date") or None
    task.save()
    messages.success(request, "Task updated!")
    return redirect("task:manage")


@login_required
@require_POST
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    messages.success(request, "Task deleted!")
    return redirect("task:manage")

@login_required
def profile_page(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    full_name = f"{user.first_name} {user.last_name}".strip()
    initials = (user.first_name[:1] + user.last_name[:1]).upper() or user.username[:2].upper()
    return render(request, "profile.html", {
        "profile": profile,
        "full_name": full_name,
        "initials": initials,
    })


@login_required
@require_POST
def profile_update(request):
    user = request.user
    parts = request.POST.get("full_name", "").strip().split(" ", 1)
    user.first_name = parts[0]
    user.last_name = parts[1] if len(parts) > 1 else ""
    user.email = request.POST.get("email", "").strip()
    user.save()

    profile, _ = Profile.objects.get_or_create(user=user)
    profile.bio = request.POST.get("bio", "").strip()
    profile.save()

    messages.success(request, "Profile updated!")
    return redirect("task:profile")


@login_required
@require_POST
def profile_password(request):
    current = request.POST.get("current_password", "")
    new = request.POST.get("new_password", "")

    if not request.user.check_password(current):
        messages.error(request, "Current password is incorrect.")
    elif len(new) < 8:
        messages.error(request, "New password must be at least 8 characters.")
    else:
        request.user.set_password(new)
        request.user.save()
        update_session_auth_hash(request, request.user)  # tizimdan chiqib ketmaslik uchun
        messages.success(request, "Password updated!")
    return redirect("task:profile")


@login_required
@require_POST
def profile_delete(request):
    user = request.user
    logout(request)
    user.delete()  # tasklar ham CASCADE bilan o'chadi
    return redirect(settings.LOGIN_URL)