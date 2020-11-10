from django.db import models
#additional import
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Report(models.Model):
    """ The report card """
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    # The title is the "object" label on the form
    title = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    venue = models.CharField(max_length=50)
    department =models.CharField(max_length=150)
    category =models.CharField(max_length=150)
    image = models.ImageField(upload_to="images",null=True, blank=True)
    #The status will be one of: unread, pending, resolved
    status = models.CharField(max_length=20,default="unread", null=True)
    pending_reason = models.CharField(max_length=200, null=True)


    def __str__(self):
        return f"{self.title} in {self.venue}"