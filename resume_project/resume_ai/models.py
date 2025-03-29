from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True)
    skills = models.JSONField(blank=True, default=list)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class CoverLetter(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_description = models.TextField()
    generated_text = models.TextField()
    edited_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)