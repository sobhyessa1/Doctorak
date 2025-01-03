from django.db import models

class AnalysisImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
