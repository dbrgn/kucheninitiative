from datetime import datetime
from django.views.generic import TemplateView, ListView
from django.contrib.auth import models as auth_models
from front import models

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
