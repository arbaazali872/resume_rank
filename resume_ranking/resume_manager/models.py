# resumes/models.py
from django.db import models
import uuid

class JobDescription(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()

class Resume(models.Model):
    session_id = models.UUIDField()
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class RankingResult(models.Model):
    session_id = models.UUIDField()
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    score = models.FloatField()
