from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField('Title', max_length=200)
    text = models.TextField('Content')
    date = models.DateTimeField('Date', default=timezone.now)

    # this is to list all related files in post_list.html
    files = GenericRelation('File')

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('Content')
    target = models.ForeignKey(Post, on_delete=models.CASCADE)


class File(models.Model):
    name = models.CharField('File Name', max_length=255)
    src = models.FileField('Attach File')

    # content_type specifies the type of models
    # object_id specifies the primary key of data
    # content_object combines them
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name
