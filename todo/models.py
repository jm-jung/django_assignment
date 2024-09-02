from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Comment(TimeStampedModel):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.todo.title} 댓글'
    class Meta:
        verbose_name='댓글'
        verbose_name_plural='댓글 목록'
        ordering=('created_at','-id')

