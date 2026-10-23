from django.urls import path
from .views import (home_page, task_mng, 
                    toggle_task, update_task, 
                    delete_task, profile_page, 
                    profile_update, profile_password, profile_delete)

app_name = "task"

urlpatterns = [
    path("", home_page, name="home"),
    path("manage/", task_mng, name="manage"),
    path("toggle/<int:pk>/", toggle_task, name="toggle"),
    path("update/<int:pk>/", update_task, name="update"),
    path("delete/<int:pk>/", delete_task, name="delete"),
    path("profile/", profile_page, name="profile"),
    path("profile/update/", profile_update, name="profile_update"),
    path("profile/password/", profile_password, name="profile_password"),
    path("profile/delete/", profile_delete, name="profile_delete"),
]