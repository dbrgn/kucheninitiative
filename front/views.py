from django.views.generic import TemplateView, ListView
from django.contrib.auth import models as auth_models
from front import models

class HomeView(TemplateView):
    template_name = 'front/home.html'

class MemberView(ListView):
    template_name = 'front/members.html'
    model = auth_models.User
