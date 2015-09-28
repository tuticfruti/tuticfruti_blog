# -*- coding: utf-8 -*-
from django import forms

from . import models


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['author', 'email', 'content']
        widgets = dict(
            author=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            email=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            content=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your comment', 'rows': 2}))
