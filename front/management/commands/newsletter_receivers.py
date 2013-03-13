# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User


class Command(NoArgsCommand):
    help = 'Return a list of all e-mail addresses of active members.'

    def handle_noargs(self, **options):
        users = User.active.all().order_by('date_joined')
        emails = []
        for user in users:
            emails.append('"{0.first_name} {0.last_name}" <{0.email}>'.format(user))
        print(', '.join(emails))
