from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    city = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    is_doctor = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    degree_certificate = models.ImageField(upload_to='certificates/%Y/%m/%d/', blank=True, null=True)
    syndicate_card = models.ImageField(upload_to='syndicate_cards/%Y/%m/%d/', blank=True, null=True)
    reset_code = models.CharField(max_length=6, blank=True, null=True)  # New field

    def __str__(self):
        return self.user.username
