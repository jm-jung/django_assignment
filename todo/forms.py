from django import forms

from todo.models import Todo, Comment


class TodoForm(forms.ModelForm):

    class Meta:
        model=Todo
        fields=('title','description','start_date','end_date')

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "start_date", "end_date", "is_completed"]


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