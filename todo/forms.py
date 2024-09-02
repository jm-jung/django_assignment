from django import forms
from django_summernote.widgets import SummernoteWidget

from todo.models import Todo, Comment


class TodoForm(forms.ModelForm):

    class Meta:
        model=Todo
        fields=('title','description','image','start_date','end_date')
        widgets={
            'description':SummernoteWidget(),
        }

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ("title", "description","image","start_date", "end_date", "is_completed")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)
        widgets={
            'message':forms.Textarea(attrs={'class':'form-control','placeholder':'댓글을 작성하세요','rows':10,'cols':20}),
        }
        labels={
            'message':'내용'
        }