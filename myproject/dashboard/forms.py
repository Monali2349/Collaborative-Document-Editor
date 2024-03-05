from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Editor


class BlogForm(forms.ModelForm):
    

    class Meta:
        model = Editor
        fields = '__all__'  # Include only the content field in the form

        

    
