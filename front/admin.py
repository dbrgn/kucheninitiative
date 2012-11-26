from django.contrib import admin
from front import models

admin.site.register(models.UserProfile)
admin.site.register(models.Assignment)
admin.site.register(models.Semester)
