from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length = 100)
    lambda_ep = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
