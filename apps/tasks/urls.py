from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('categorias/', views.list_categories, name='list_categories'),
    path('categorias/adicionar/', views.add_category, name='add_category'),
    path('categorias/editar/<int:id_category>',
         views.edit_category, name='edit_category'),
    path('categorias/excluir/<id_category>',
         views.delete_category, name='delete_category'),

    path('', views.list_tasks, name='list_tasks'),
    path('adicionar/', views.add_task, name='add_task'),
    path('editar/<int:id_task>', views.edit_task, name='edit_task'),
    path('excluir/<int:id_task>', views.delete_task, name='delete_task'),
    path('complete/<int:id_task>', views.complete_task, name='complete_task'),
    path('revert/<int:id_task>', views.not_complete_task, name='descomplete_task'),
    path('show_task/<int:id_task>', views.show_task, name='show_task'),
    path('show_completed_tasks/', views.show_completed_tasks,
         name='show_completed_tasks'),

    path('low_priority_tasks/', views.low_priority_tasks,
         name='low_priority_tasks'),
    path('medium_priority_tasks/', views.medium_priority_tasks,
         name='medium_priority_tasks'),
    path('high_priority_tasks/', views.high_priority_tasks,
         name='high_priority_tasks'),

    path('imcomplete_tasks/', views.imcomplete_tasks,
         name='imcomplete_tasks'),
     path('filtro/', views.task_filter,
         name='task_filter'),

]
