from django.contrib import admin

from schedule.models import Section


class SectionAdmin(admin.ModelAdmin):
    search_fields = ("code", "lecturer")


admin.site.register(Section, SectionAdmin)
