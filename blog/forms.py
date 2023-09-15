from django import forms

from blog.models import Blog
from services.forms import FormStyleMixin


class BlogCreateForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('name', 'content', 'image')
