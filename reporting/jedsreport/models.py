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
    status_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} in {self.venue}"

class Resolved(models.Model):
    """ These are the solved reports  """
    report = models.OneToOneField(Report, primary_key=True, on_delete=models.CASCADE, related_name="report_solution")
    timestamp = models.DateTimeField(auto_now_add=True)
    who = models.CharField(max_length=200, null=True)
    cost = models.IntegerField(null=True)
    comment = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f"resolved by: {self.who} on {self.timestamp}"

class Pending(models.Model):
    """ These are the pending reports """
    report = models.OneToOneField(Report, primary_key=True, on_delete=models.CASCADE, related_name="pending_report")
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    reason = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f"since: {self.timestamp}, {self.reason}"
