from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event,Vanue
from .forms import VanueForm,EventForm
# Create your views here.

def delete_vanue(request,vanue_id):
    vanue = Vanue.objects.get(pk=vanue_id)
    vanue.delete()
    return redirect('list_vanue')
def delete_event(request,event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list_events')

def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html',{'form':form,'submitted':submitted})

def update_event(request,event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None,instance=event)
    if form.is_valid():
        form.save()
        return redirect('list_events')

    return render(request,'events/update_event.html',{'event':event,'form':form})

def update_vanue(request,vanue_id):
    vanue = Vanue.objects.get(pk=vanue_id)
    form = VanueForm(request.POST or None,request.FILES or None,instance=vanue)
    if form.is_valid():
        form.save()
        return redirect('list_vanue')

    return render(request,'events/update.html',{'vanue':vanue,'form':form})


def search_vanue(request):
    if request.method == "POST":
        searched = request.POST['searched']
        vanue = Vanue.objects.filter(name__contains = searched)
        return render(request, 'events/search_vanue.html',{'searched':searched,'vanue':vanue})
    else:
        return render(request, 'events/search_vanue.html')

def show_vanue(request,vanue_id):
    vanue = Vanue.objects.get(pk=vanue_id)
    return render(request,'events/show_vanue.html',{'vanue':vanue})


def list_vanue(request):
    vanue_list = Vanue.objects.all()
    return render(request, 'events/vanue.html', {'vanue_list': vanue_list})

def add_vanue(request):
    submitted = False
    if request.method == "POST":
        form = VanueForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_vanue?submitted=True')
    else:
        form = VanueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_vanue.html',{'form':form,'submitted':submitted})


def all_events(request):
    event_list = Event.objects.all()
    return render(request,'events/event_list.html',{'event_list':event_list})


def home(request,year=datetime.now().year,month=datetime.now().strftime('%B')):
    name = "Sakib"
    month = month.capitalize()
    month_number=list(calendar.month_name).index(month)
    month_number  = int(month_number)

    cal = HTMLCalendar().formatmonth(year,month_number)

    now = datetime.now()
    current_year= now.year
    time = now.strftime('%I:%M:%p')
    return render(request,'events/home.html',{
        "name":name,
        "year":year,
        "month":month,
        "month_number":month_number,
        "cal":cal,
        "current_year":current_year,
        "time":time,
    })