from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name="home"),
    path('home/<int:year>/<str:month>',views.home,name="homeYM"),
    path('events',views.all_events,name="list_events"),
    path('add_vanue',views.add_vanue,name="add_vanue"),
    path('list_vanue',views.list_vanue,name="list_vanue"),
    path('show_vanue/<vanue_id>',views.show_vanue,name='show_vanue'),
    path('search_vanue',views.search_vanue,name="search_vanue"),
    path('update_vanue/<vanue_id>',views.update_vanue,name="update_vanue"),
    path('update_event/<event_id>', views.update_event, name="update_event"),
    path('add_event',views.add_event,name="add_event"),
    path('delete_event/<event_id>',views.delete_event,name="delete_event"),
    path('delete_vanue/<vanue_id>', views.delete_vanue, name="delete_vanue"),
    path('vanue_text',views.vanue_text,name='vanue_text'),
    path('vanue_csv',views.vanue_csv,name='vanue_csv'),
    path('vanue_pdf',views.vanue_pdf,name='vanue_pdf'),
    path('my_events',views.my_events,name='my_events'),
    path('search_events',views.search_events,name='search_events'),
    path('admin_approval',views.admin_approval,name='admin_approval'),
]