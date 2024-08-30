from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse

from todo.forms import TodoForm
from todo.models import Todo


class TodoListView(LoginRequiredMixin, ListView):
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

class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo_info.html'
    context_object_name = 'todo'
    pk_url_kwarg = 'todo_pk'  # URL에서 사용하는 파라미터 이름을 지정

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo:info'] = self.object  # 'todo:info'를 그대로 사용
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
    pk_url_kwarg = 'todo_pk'
    def get_object(self,queryset=None):
        todo = super().get_object(queryset)
        if todo.author != self.request.user:
            raise Http404()
        return todo
    def get_success_url(self):
        return reverse('todo:list')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['sub_title']='수정'
        context['btn_name']='수정'
        return context

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self):
        pk = self.kwargs.get('pk')
        todo = get_object_or_404(Todo, pk=pk)
        if todo.author != self.request.user:
            raise Http404()
        return todo
    def get_success_url(self):
        return reverse('todo:list')

