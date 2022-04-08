from django.contrib import admin

from .models import RequestPerformanceLog, Config


class RequestPerformanceLogAdmin(admin.ModelAdmin):
    list_display = ('time_consume', 'method', 'path', 'file_path', 'hit_num', 'threshold', 'updated_at', 'created_at', 'alerted')


admin.site.register(RequestPerformanceLog, RequestPerformanceLogAdmin)
admin.site.register(Config)
