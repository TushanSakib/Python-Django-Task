from django.contrib import admin
from .models import Vanue,MyClubUser,Event
from django.contrib.auth.models import Group
# Register your models here.
#admin.site.register(Vanue)
admin.site.register(MyClubUser)

#Remove Groups
#admin.site.unregister(Group)

#admin.site.register(Event)

@admin.register(Vanue)
class VanueAdmin(admin.ModelAdmin):
    list_display = ('name','address','phone')
    ordering = ('name',)
    search_fields = ('name','address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name','vanue'),'event_date','description','manager','approved')
    list_display = ('name','event_date','vanue')
    list_filter = ('event_date','vanue')
    ordering = ('-event_date',)