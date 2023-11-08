from django.db import models

# Define a new Django model named RequestAndAnswer with three fields
class RequestAndAnswer(models.Model):
    request = models.TextField()  # A text field to store the request information
    answer = models.TextField()   # A text field to store the answer for the request
    username = models.TextField(default="test")  # A text field to store the username associated with the request and answer