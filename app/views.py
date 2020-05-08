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
