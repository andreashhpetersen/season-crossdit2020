from django.contrib import admin
from backend.models import Field, FieldAnalysis, Crop, Monitoring


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    pass


@admin.register(FieldAnalysis)
class FieldAnalysisAdmin(admin.ModelAdmin):
    pass

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    pass

admin.site.register(Monitoring)
