from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    text = models.TextField()
    created_by = models.ForeignKey(User,on_delete = models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class DocMember(models.Model): 
    userId = models.ForeignKey(User,on_delete = models.CASCADE)
    doc_ID = models.ForeignKey(Document,on_delete = models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    approve = models.BooleanField(default=True)    

    