from .models import Post
from django import forms
from django.utils.translation import gettext_lazy


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        label = {
            'text': gettext_lazy('Текст поста')
        }
        help_text = {
            'group': gettext_lazy('Группа поста')
        }
