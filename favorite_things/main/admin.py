from django.contrib import admin

from main.models import FavThing, ThingCategory, LogAction

admin.site.register(FavThing)
admin.site.register(ThingCategory)
admin.site.register(LogAction)
