# Django_Generic_Inlineformset_Factory

[referred blog](https://narito.ninja/blog/detail/34/)

![generic-inlineformset-factory](generic-inlineformset-factory.gif)

> ## models.py
``` python
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
```

> ## forms.py
``` python
from django import forms
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from .models import Post, File


class PostCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Post
        fields = '__all__'


FileInlineFormSet = generic_inlineformset_factory(
    File, fields='__all__', can_delete=False, extra=3,
)

# FileInlineFormSet above is a formset that displays files inline
# generic_inlineformset_factory is almost same as inlineformset_factory, but
# it requires only one models (in this case, File)
```


> ## views.py
``` python
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import PostCreateForm, FileInlineFormSet
from .models import Post


class PostList(generic.ListView):
    model = Post

# the view that uses generic_inlineformset_factory is the exactly same as the view that uses inlineformset_factory
def add_post(request):
    form = PostCreateForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        formset = FileInlineFormSet(request.POST, files=request.FILES, instance=post)
        if formset.is_valid():
            post.save()
            formset.save()
            return redirect('app:index')

        # we store formset with error message in context and it will be passed to template.
        else:
            context['formset'] = formset

    # GET, when we first go to 'add_post' url (add_post view), there is no data in context
    # so we set empty context below. By doing this, contents of formset can be displayed in post_list.html
    else:
        # show update page again here
        context['formset'] = FileInlineFormSet()

    return render(request, 'app/post_form.html', context)


def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostCreateForm(request.POST or None, instance=post)
    formset = FileInlineFormSet(request.POST or None, files=request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        form.save()
        formset.save()
        
        return redirect('app:update_post', pk=pk)

    context = {
        'form': form,
        'formset': formset
    }

    return render(request, 'app/post_form.html', context)
```

> ## urls.py
``` python

```

> ## admin.py
``` python

```
