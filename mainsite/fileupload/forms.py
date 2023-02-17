# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File Name：   forms
  Description : MiniMES Company
  Author :    Karo Lin
  date：     2022/10/8
  Copyright follow MIT definitions.
-------------------------------------------------
  Change Activity:
          2022/10/8:
-------------------------------------------------
"""
__author__ = 'Karo Lin'

from django import forms
from django.forms import TextInput, FileInput, Textarea
from .models import UploadIcons


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Image',
                           widget=(
                               forms.FileInput(
                                   attrs={'class': 'form-control', 'accept': 'image/*'}
                               )
                           )

                           )


class UploadIconModelForm(forms.ModelForm):
    class Meta:
        model = UploadIcons
        fields = ['Title', 'IconImage', 'Description']
        labels = {
            'Title': 'Icon Title',
            'Description': 'Description',
            'IconImage': 'Icon Photo',
        }
        widgets = {
            'Title': TextInput(attrs={'class': 'form-control', 'id': 'title'}),
            'Description': Textarea(attrs={'class': 'form-control', 'id': 'description', 'rows': '4'}),
            'IconImage': FileInput(attrs={'class': 'form-control mb-3', 'id': 'upload_icon', 'onchange': 'ShowName()'}),
        }
