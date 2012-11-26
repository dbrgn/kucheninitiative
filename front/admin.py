from reversion import VersionAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import models as auth_models
from front import models


# User management

class UserProfileInline(admin.StackedInline):
    model = models.UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(auth_models.User)
admin.site.register(auth_models.User, UserAdmin)


# Other model admin registrations

class AssignmentAdmin(VersionAdmin):
    pass


class SemesterAdmin(VersionAdmin):
    pass


admin.site.register(models.Assignment, AssignmentAdmin)
admin.site.register(models.Semester, SemesterAdmin)
