from datetime import datetime
from collections import defaultdict
from django.views.generic import TemplateView, ListView
from django.contrib.auth import models as auth_models
from front import models
from lib.utils import daterange


class HomeView(TemplateView):
    template_name = 'front/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['switch'] = datetime.now().second % 2
        return context


class MemberView(ListView):
    template_name = 'front/members.html'
    queryset = auth_models.User.objects.all().order_by('pk')


class RuleView(TemplateView):
    template_name = 'front/rules.html'


class ScheduleView(TemplateView):
    template_name = 'front/schedule.html'

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)

        # Get all semesters
        semesters = models.Semester.objects.all()

        # Get all possible dates in that semester
        context['semesters'] = []
        for semester in semesters:
            dates = daterange(semester.start_date, semester.end_date)
            context['semesters'].append((semester, dates))

        # Get all assignments, group by date
        assignments = defaultdict(list)
        for assignment in models.Assignment.objects.order_by('date', 'User__username'):
            assignments[assignment.date].append(assignment.User.name())
        context['assignments'] = assignments

        return context
