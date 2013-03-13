# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from datetime import date

from django.db import models
from django.contrib.auth import models as auth_models


# Managers

class CurrentSemesterManager(models.Manager):
    """A  manager that returns all assignments in the current semester."""

    def get_query_set(self):
        # Get current semester
        future_semesters = Semester.objects.filter(end_date__gte=date.today())
        semester = future_semesters.order_by('start_date')[0]
        # Filter assignments by semester
        return super(CurrentSemesterManager, self) \
                    .get_query_set() \
                    .filter(date__gte=semester.start_date, date__lte=semester.end_date)


class ActiveUsersManager(models.Manager):
    """A  manager that returns only active users."""

    def get_query_set(self):
        return super(ActiveUsersManager, self).get_query_set().filter(is_active=True)


# Models

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
    user = models.OneToOneField(auth_models.User)
    course = models.CharField(u'Studiengang', max_length=3, choices=COURSE_CHOICES)
    phone = models.CharField(u'Natel', max_length=13, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Benutzerprofil'
        verbose_name_plural = 'Benutzerprofile'


class Assignment(models.Model):
    User = models.ForeignKey(auth_models.User)
    date = models.DateField(u'datum')
    unfulfilled = models.BooleanField(u'nicht erfüllt', default=False)
    photo = models.ImageField(u'foto', upload_to='photos', null=True, blank=True,
            help_text=u'Ein Beweisfoto des Kuchens.')

    objects = models.Manager()
    current_semester = CurrentSemesterManager()

    def __unicode__(self):
        return '%s: %s' % (self.date, self.User.username)

    class Meta:
        verbose_name = 'Termin'
        verbose_name_plural = 'Termine'
        unique_together = ('User', 'date')
        ordering = ['-date']


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

    def assignments(self):
        return Assignment.objects.filter(date__lte=self.start_date, date__gte=self.start_date)

    def __unicode__(self):
        return '%ss %s' % (self.season, self.year)

    class Meta:
        verbose_name = 'Semester'
        verbose_name_plural = 'Semester'
        unique_together = ('year', 'season')
        ordering = ['start_date']


# User model functions

def name(self):
    """Return either full user first and last name or the username, if no
    further data is found."""
    if self.first_name or self.last_name:
        return ' '.join(filter(None, [self.first_name, self.last_name]))
    return self.username
auth_models.User.add_to_class('name', name)
auth_models.User.add_to_class('objects', models.Manager())
auth_models.User.add_to_class('active', ActiveUsersManager())
