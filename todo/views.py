from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Todo

def todo(request):
    todos=Todo.objects.all()
    context={'todos':todos}
    return render(request,'todo.html',context)

def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    context = {'todo': todo}
    return render(request, 'todo_info.html', context)
# Create your views here.
