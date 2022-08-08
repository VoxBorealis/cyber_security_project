from django.db import models
from sqlalchemy import true


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=100)

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    task_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date added', auto_now_add=true)
    
