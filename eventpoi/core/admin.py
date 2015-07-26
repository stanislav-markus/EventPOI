from django.contrib import admin
from core.models import POI

class POIAdmin(admin.ModelAdmin):
    exclude = ('date', 'user', 'slug',)

    def save_model(self, request, obj, form, change): 
        obj.user = request.user
        obj.save()

admin.site.register(POI, POIAdmin)
