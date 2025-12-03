from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True)
    is_cuidador = models.BooleanField(default=False)
    is_familiar = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user.get_full_name()}"