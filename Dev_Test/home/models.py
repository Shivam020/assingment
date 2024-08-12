# home/models.py
from django.db import models
from django.utils import timezone


# home/models.py
class UploadedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Update field

    def __str__(self):
        return self.file.name
