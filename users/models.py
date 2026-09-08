from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	phone_number = models.CharField(max_length=11)
	last_name = models.CharField(max_length=100)
