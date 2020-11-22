from django.contrib import admin

# Register your models here.
from .models import Report, Pending, Resolved, User

admin.site.register(Report)
admin.site.register(Pending)
admin.site.register(Resolved)
admin.site.register(User)