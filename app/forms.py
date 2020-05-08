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