from django.db import models

from mdeditor.fields import MDTextField
# Create your models here.


class Announcement(models.Model):
    post = MDTextField()

    def __str__(self):
        return 'announcement'
