from .models import Task

def task(request):
    context = {
        "task": Task.objects.filter(user_id=request.user.id).all()
    }
    return context