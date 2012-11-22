# coding=utf-8

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
    course = models.CharField(u'Studiengang', max_length=3, choices=COURSE_CHOICES)
    phone = models.CharField(u'Natel', max_length=13, null=True, blank=True)

    def __unicode__(self):
        return self.user.username


class Semester(models.Model):
    SEASON_CHOICES = (
        ('H', 'Herbstsemester'),
        ('F', 'Frühlingssemester'),
    )
    year = models.PositiveIntegerField(u'Jahr')
    season = models.CharField(u'Semester', max_length=1, choices=SEASON_CHOICES)
    start_date = models.DateField(u'Semesterbeginn')
    end_date = models.DateField(u'Semesterende')
    weekdays = models.CommaSeparatedIntegerField(u'Kuchentage', max_length=9, null=True, blank=True,
            help_text=u'Kommagetrennte Liste der Wochentage (1-5), an welchen es Kuchen gibt.')

    def weekday_list(self):
        return [int(day) for day in self.weekdays.split(',')]
    
    def __unicode__(self):
        return '%ss %s' % (self.season, self.year)

    class Meta:
        unique_together = ('year', 'season')
        ordering = ['start_date']
