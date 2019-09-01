from django.contrib import admin

from schedule.models import Building, Program, Section


class BuildingAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


class ProgramAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


class SectionAdmin(admin.ModelAdmin):
    search_fields = ("code", "lecturer")


admin.site.register(Building, BuildingAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Section, SectionAdmin)
