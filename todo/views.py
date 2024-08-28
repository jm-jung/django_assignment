from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .forms import TodoForm
from .models import Todo

def todo(request):
    todos=Todo.objects.all()
    q=request.GET.get('q')
    if q:
        todos=todos.filter(
            Q(title__icontains=q)|
            Q(description__icontains=q)|
            Q(author__username__icontains=q)
        )


    paginator=Paginator(todos,10)
    page=request.GET.get('page')
    page_object=paginator.get_page(page)

    context={'todos':todos
             ,'page_object':page_object}
    return render(request,'todo.html',context)
@login_required
def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    context = {'todo': todo}
    return render(request, 'todo_info.html', context)
# Create your views here.

@login_required
def todo_create(request):
    form=TodoForm(request.POST or None)
    if form.is_valid():
        todo=form.save(commit=False)
        todo.author=request.user
        todo.save()

        return redirect(reverse('todo_info',kwargs={'todo_id':todo.id}))
    context={'form':form}
    return render(request,'todo_create.html',context)

@login_required
def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id,author=request.user)
    form=TodoForm(request.POST or None, instance=todo)
    if form.is_valid():
        todo=form.save()
        return redirect(reverse('todo_info',kwargs={'todo_id':todo.id}))
    context={'form':form}
    return render(request,'todo_update.html',context)

@login_required
@require_http_methods(['POST'])
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo,pk=todo_id)
    todo.delete()
    return redirect(reverse('todo'))