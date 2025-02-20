from django.contrib import admin

from Luna.models import HydroponicSystem, Reading


# Register your models here.
@admin.register(HydroponicSystem)
class HydroponicSystemAdmin(admin.ModelAdmin):
    pass


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    pass
