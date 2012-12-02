from datetime import date, datetime
from collections import defaultdict
from django.views.generic import TemplateView, ListView
from django.contrib.auth import models as auth_models
from front import models
from lib.utils import daterange
from lib.mixins import LoginRequiredMixin


class HomeView(TemplateView):
    template_name = 'front/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['switch'] = datetime.now().second % 2
        return context


class MemberView(LoginRequiredMixin, ListView):
    template_name = 'front/members.html'
    queryset = auth_models.User.objects.all().order_by('pk')


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
