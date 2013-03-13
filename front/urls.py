from django.conf.urls import patterns, include, url
from front import views

urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^members/$', views.MemberView.as_view(), name='members'),
    url(r'^rules/$', views.RuleView.as_view(), name='rules'),
    url(r'^schedule/$', views.ScheduleView.as_view(), name='schedule'),
    url(r'^gallery/$', views.GalleryView.as_view(), name='gallery'),
    url(r'^stats/$', views.StatsView.as_view(), name='stats'),

    url(r'^charts/members_per_course/$', views.members_per_course, name='chart_members_by_course'),
    url(r'^charts/cakes_per_member/$', views.cakes_per_member, name='chart_cakes_per_member'),
)
