from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse

from todo.forms import TodoForm, CommentForm
from todo.models import Todo, Comment


class TodoListView(ListView):
    queryset = Todo.objects.all()
    ordering = ('-created_at',)
    template_name = 'todo.html'
    paginate_by=10
    def get_queryset(self):
        queryset=super().get_queryset()
        q=self.request.GET.get('q')
        if q:
            return queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(author__username__icontains=q)
            )
        return queryset

class TodoDetailView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'todo_info.html'
    paginate_by = 10  # URL에서 사용하는 파라미터 이름을 지정
    def get(self,request,*args,**kwargs):
        self.object=get_object_or_404(Todo,pk=kwargs.get('todo_pk'))
        return super().get(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form']=CommentForm()
        context['todo'] = self.object  # 'todo:info'를 그대로 사용
        return context
class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo_form.html'
    form_class = TodoForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['sub_title']='작성'
        context['btn_name']='등록'
        return context
    def get_success_url(self):
        return reverse('todo:list')

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'todo_form.html'
    form_class = TodoForm
    def get_object(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['sub_title']='수정'
        context['btn_name']='수정'
        return context

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    def get_object(self):
        queryset=super().get_queryset()
        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        return queryset
    def get_success_url(self):
        return reverse('todo:list')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def get(self,*args,**kwargs):
        raise Http404
    def form_valid(self, form):
        todo=self.get_todo()
        self.object = form.save(commit=False)
        self.object.user=self.request.user
        self.object.todo=todo
        self.object.save()
        return HttpResponseRedirect(reverse('todo:info',kwargs={'todo_pk':todo.pk}))

    def get_todo(self):
        pk=self.kwargs['todo_pk']
        todo=get_object_or_404(Todo, pk=pk)
        return todo

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)  # 'author'를 'user'로 변경

    def get_success_url(self):
        return reverse('todo:info', kwargs={'todo_pk': self.object.todo.pk})

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'todo_info.html'  # 템플릿 이름 추가

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)  # 'author'를 'user'로 변경

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = self.object.todo  # todo 객체를 컨텍스트에 추가
        return context
    def get_success_url(self):
        return reverse('todo:info', kwargs={'todo_pk': self.object.todo.pk})