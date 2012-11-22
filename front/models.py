from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    COURSE_CHOICES = (
        ('I', 'Informatik'),
        ('E', 'Elektrotechnik'),
        ('L', 'Landschaftsarchitektur'),
        ('R', 'Raumplanung'),
        ('M', 'Maschinentechnik'),
        ('B', 'Bauingenieurwesen'),
        ('EEU', 'Erneuerbare Energien'),
    )
    user = models.OneToOneField(User)
    course = models.CharField(max_length=3, choices=COURSE_CHOICES)
    phone = models.CharField(max_length=13, unique=True, null=True, blank=True)

    def __unicode__(self):
        return self.user.username
