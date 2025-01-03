from django.db import models
from django.contrib.auth.models import User

class Disease(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    disease_name = models.CharField(max_length=100)
    treatment_start_date = models.DateField()
    recovery_date = models.DateField(null=True)
    modified_dates = models.TextField(null=True)
    def __str__(self):
        return self.disease_name

class PrescriptionImage(models.Model):
    disease = models.ForeignKey(Disease, related_name='prescription_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='prescriptions/%Y/%m/%d/')

class AnalysisImage(models.Model):
    disease = models.ForeignKey(Disease, related_name='analysis_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='analysis/%Y/%m/%d/')