from django.contrib import admin
from .models import Worklist, Limits, RunRecovery


class WorklistAdmin(admin.ModelAdmin):
    pass


class LimitsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Worklist, WorklistAdmin)
admin.site.register(Limits, LimitsAdmin)
admin.site.register(RunRecovery)

