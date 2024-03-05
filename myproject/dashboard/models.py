from django.db import models
from ckeditor.fields import RichTextField

class Editor(models.Model):
    content = RichTextField()
