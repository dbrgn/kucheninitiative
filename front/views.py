# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import json
from datetime import date, datetime
from collections import defaultdict
from operator import itemgetter

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.db.models import Count
from django.contrib.auth import models as auth_models

from lib.utils import daterange
from lib.mixins import LoginRequiredMixin

from front import models


class HomeView(TemplateView):
    template_name = 'front/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['switch'] = datetime.now().second % 2
        context['membercount'] = auth_models.User.active.count()
        return context


class MemberView(LoginRequiredMixin, ListView):
    template_name = 'front/members.html'
    queryset = auth_models.User.active.order_by('pk')


class RuleView(TemplateView):
    template_name = 'front/rules.html'


class ScheduleView(TemplateView):
    template_name = 'front/schedule.html'

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)

        # Get current semester
        future_semesters = models.Semester.objects.filter(end_date__gte=date.today())
        semester = future_semesters.order_by('start_date')[0]

        # Get all possible dates in that semester
        context['semesters'] = []
        dates = daterange(semester.start_date, semester.end_date)
        context['semesters'].append((semester, dates))

        # Get all assignments, group by date
        assignments = defaultdict(list)
        for assignment in models.Assignment.objects.order_by('date', 'User__username'):
            assignments[assignment.date].append(assignment.User.name())
        context['assignments'] = assignments

        return context


class StatsView(TemplateView):
    template_name = 'front/stats.html'

    def get_context_data(self, **kwargs):
        context = super(StatsView, self).get_context_data(**kwargs)
        context['membercount'] = auth_models.User.active.count()
        return context


# JSON data views

def handle_chart_json(request, data):
    if settings.DEBUG or request.is_ajax():
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse('Access via AJAX only.', status=403)


def members_per_course(request):
    """Return members per course for the current semester."""
    course_dict = dict(models.UserProfile.COURSE_CHOICES)
    data = list(models.UserProfile.objects.values('course')
                                  .filter(user__is_active=True)
                                  .annotate(mcount=Count('course'))
                                  .order_by('-mcount'))
    for course in data:
        course['course_full'] = course_dict[course['course']]
    return handle_chart_json(request, data)


def cakes_per_member(request):
    """Return cakes per member for the current semester."""
    users = list(auth_models.User.active
                                 .values('id', 'first_name', 'last_name')
                                 .order_by('first_name'))
    data = {
        a['User']: a['ccount']
        for a in models.Assignment.current_semester
                                 .filter(unfulfilled=False, date__lte=date.today())
                                 .values('User')
                                 .annotate(ccount=Count('User'))
    }
    for user in users:
        user['ccount'] = data.get(user['id'], 0)
        del user['id']
    data = sorted(users, key=itemgetter('ccount'), reverse=True)
    return handle_chart_json(request, data)
