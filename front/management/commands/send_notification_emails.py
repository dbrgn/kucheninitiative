# coding=utf-8
from datetime import date, timedelta
from django.core.management.base import NoArgsCommand
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from front.models import Assignment

WEEKDAYS = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']


class Command(NoArgsCommand):
    help = 'Send notification emails to people that have to bake in 2 days.'

    def handle_noargs(self, **options):
        notification_date = date.today() + timedelta(2)
        assignments = Assignment.objects.filter(date=notification_date)

        template = get_template('front/email/notification_email.txt')

        for assignment in assignments:
            weekday = WEEKDAYS[assignment.date.weekday()]
            sender = 'dbargen@hsr.ch'
            receiver = assignment.User.email
            subject = 'Erinnerung: Kuchen am %s!' % weekday
            fellow_bakers = [a.User.name() for a in assignments.exclude(pk=assignment.pk)]
            message = template.render(Context({
                'assignment': assignment,
                'weekday': weekday,
                'fellow_bakers': fellow_bakers,
            }))
            if not receiver:
                print 'No email available for %s.' % assignment.User.name()
                continue
            print 'Sending email to %s...' % receiver
            #send_mail(subject, message, sender, [receiver])

        print 'Sent notifications to %u users.' % len(assignments)
