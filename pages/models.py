from django.db import models

class RequestAndAnswer(models.Model):
    request = models.TextField()
    answer = models.TextField()
    username = models.TextField(default="test")