from django.db import models
from .utility import get_file_path


class UploadIcons(models.Model):
    Title = models.CharField(max_length=32, verbose_name='Icon Title')
    Description = models.CharField(max_length=256, verbose_name='Description', default='Add Description...')
    IconImage = models.ImageField(upload_to=get_file_path, verbose_name='Icon')
