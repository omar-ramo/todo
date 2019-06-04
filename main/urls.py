from django.urls import path, include

from . import views

app_name = 'main'
urlpatterns = [
    path('<slug:task_slug>/', include([
        path('update/', views.task_update, name='task_update'),
        path('delete/', views.task_delete, name='task_delete'),
        path('do/', views.task_do, name='task_do'),
        path('undo/', views.task_undo, name='task_undo'),
        path('detail/', views.task_detail, name='task_detail'),

    ])),
    path('done-tasks/', views.done_task_list, name='done_task_list'),
    path('add/', views.task_create, name='task_create'),
    path('', views.task_list, name='task_list'),
]
