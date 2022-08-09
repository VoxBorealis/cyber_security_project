from django.urls import path

from .views import index, logout, register, new_task, task, search_tasks

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('new_task/', new_task, name='new_task'),
    path('task/<int:id>/', task, name='task'),
    path('search_tasks/', search_tasks, name='search_tasks')
]