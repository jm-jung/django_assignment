from django.urls import path
from . import views
from .cb_views import TodoListView, TodoDetailView, TodoCreateView, TodoUpdateView, TodoDeleteView, CommentCreateView, \
    CommentUpdateView, CommentDeleteView

app_name = 'todo'
urlpatterns = [
    # path('', views.todo, name='todo'),
    # path('<int:todo_id>/', views.todo_info, name='todo_info'),
    # path('create/',views.todo_create, name='todo_create'),
    # path('<int:todo_id>/update', views.todo_update, name='todo_update'),
    # path('<int:todo_id>/delete', views.todo_delete, name='todo_delete'),

    path('', TodoListView.as_view(), name='list'),
    path('<int:todo_pk>/', TodoDetailView.as_view(), name='info'),
    path('create/',TodoCreateView.as_view(), name='create'),
    path('<int:pk>/update/', TodoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TodoDeleteView.as_view(), name='delete'),
    path('comment/create/<int:todo_pk>/',CommentCreateView.as_view(), name='comment_create'),
    path('comment/update/<int:pk>/',CommentUpdateView.as_view(), name='comment_update'),
    path('comment/delete/<int:pk>/',CommentDeleteView.as_view(), name='comment_delete'),
]