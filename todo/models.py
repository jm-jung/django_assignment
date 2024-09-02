from PIL import Image
from io import BytesIO
from pathlib import Path
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse

class Todo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField('이미지', null=True, blank=True, upload_to='todo/%Y/%m/%d/')
    thumbnail = models.ImageField('썸네일', null=True, blank=True, upload_to='todo/%Y/%m/%d/thumbnail')

    def __str__(self):
        return self.title

    def get_absolute_url(self):

        return reverse('todo:info', kwargs={'todo_pk': self.pk})

    def get_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        return None

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)

        image = Image.open(self.image)
        image.thumbnail((300, 300))
        image_path = Path(self.image.name)

        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix.lower()
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}'

        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)
        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)

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

