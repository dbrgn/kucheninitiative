from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    COURSE_CHOICES = (
        ('B', 'Bauingenieurwesen'),
        ('E', 'Elektrotechnik'),
        ('EEU', 'Erneuerbare Energien'),
        ('I', 'Informatik'),
        ('L', 'Landschaftsarchitektur'),
        ('M', 'Maschinentechnik'),
        ('R', 'Raumplanung'),
    )
    user = models.OneToOneField(User)
    course = models.CharField(max_length=3, choices=COURSE_CHOICES)
    phone = models.CharField(max_length=13, null=True, blank=True)

    def __unicode__(self):
        return self.user.username
