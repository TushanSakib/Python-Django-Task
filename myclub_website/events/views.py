from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event,Vanue,MyClubUser
from .forms import VanueForm,EventForm,EventFormAdmin
from django.http import HttpResponse
from django.contrib import messages
import csv
#Package for PDF file
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
#Import Pagination staff
from django.core.paginator import Paginator
# Create your views here.

#Create my events page
def my_events(request):
    if request.user.is_authenticated:
        events = Event.objects.filter(attendees=request.user.id)
        return render(request, 'events/my_events.html', {'events': events})
    else:
        messages.success(request,"You are not authorized to view this page")
        return redirect('home')




#Generate a PDF Files
def vanue_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter,bottomup=0)
    #Create text object
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)

    #Add some line of text
    lines = []
    vanue =Vanue.objects.all()
    for vanue in vanue:
        lines.append(vanue.name)
        lines.append(vanue.address)
        lines.append(vanue.zip_code)
        lines.append(vanue.phone)
        lines.append(vanue.web)
        lines.append(vanue.email_address)
        #lines.append(vanue.vanue_image)
        lines.append(" ")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf,as_attachment=True,filename='vanue.pdf')

def vanue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=vanue.csv'
    #Create csv writer
    writer = csv.writer(response)
    #Designate The model
    vanue = Vanue.objects.all()
    #Add column heading to csv file
    writer.writerow(['Vanue Name','Address','Zip-Code','Phone','Web','Email Address'])

    for vanue in vanue:
        writer.writerow([vanue.name,vanue.address,vanue.zip_code,vanue.phone,vanue.web,vanue.email_address])

    return response



def vanue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=vanue.txt'
    vanue = Vanue.objects.all()
    lines = []
    for vanue in vanue:
        lines.append(f'{vanue.name}\n{vanue.address}\n{vanue.zip_code}\n{vanue.phone}\n{vanue.web}\m{vanue.email_address}')
    #lines = ["This is line 1\n",
     #        "This is line 2\n",
      #       "This is line 3\n"]
    response.writelines(lines)
    return response

def delete_vanue(request,vanue_id):
    vanue = Vanue.objects.get(pk=vanue_id)
    vanue.delete()
    return redirect('list_vanue')
def delete_event(request,event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
       event.delete()
       messages.success(request, "Boom!!! Event deleted")

       return redirect('list_events')
    else:
        messages.success(request,"Trying to delete hack!! hahahaha!!!You are not authorized to delete this!!")
    return redirect('list_events')

def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')


    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html',{'form':form,'submitted':submitted})

def update_event(request,event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None,instance=event)
    else:
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

def search_events(request):
    if request.method == "POST":
        searched = request.POST['searched']
        events = Event.objects.filter(description__contains = searched)
        return render(request, 'events/search_events.html',{'searched':searched,'events':events})
    else:
        return render(request, 'events/search_events.html')
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
    #vanue_list = Vanue.objects.all().order_by('?')
    vanue_list = Vanue.objects.all()

    #Set up Pagination
    p = Paginator(Vanue.objects.all(),1)
    page = request.GET.get('page')
    vanues = p.get_page(page)
    nums = "a" * vanues.paginator.num_pages
    return render(request, 'events/vanue.html', {'vanue_list': vanue_list,'vanues':vanues,'nums':nums})

def add_vanue(request):
    submitted = False
    if request.method == "POST":
        form = VanueForm(request.POST,request.FILES)
        if form.is_valid():
            vanue = form.save(commit=False)
            vanue.owner = request.user.id
            vanue.save()
            return HttpResponseRedirect('/add_vanue?submitted=True')
    else:
        form = VanueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_vanue.html',{'form':form,'submitted':submitted})


def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    return render(request,'events/event_list.html',{'event_list':event_list})

def admin_approval(request):
    venue_list = Vanue.objects.all()
    event_count= Event.objects.all().count()
    venue_count= Vanue.objects.all().count()
    user_count= MyClubUser.objects.all().count()

    admin_approval_list = Event.objects.all()
    if request.user.is_superuser:
     if request.method == "POST":
        id_list = request.POST.getlist("boxes")
        admin_approval_list.update(approved=False)
        #Update database
        for x in id_list:
            Event.objects.filter(pk=int(x)).update(approved=True)
        return redirect('list_events')
     else:
        return render(request, 'events/admin_approval.html', {'admin_approval_list': admin_approval_list,
                                                              'event_count':event_count,'venue_count':venue_count,'user_count':user_count,
                                                              'venue_list':venue_list})


def home(request,year=datetime.now().year,month=datetime.now().strftime('%B')):
    name = "Sakib"
    month = month.capitalize()
    month_number=list(calendar.month_name).index(month)
    month_number  = int(month_number)

    cal = HTMLCalendar().formatmonth(year,month_number)

    now = datetime.now()
    current_year= now.year
    #Qyery the events model by Dates
    event_list = Event.objects.filter(
        event_date__year = year,
        event_date__month = month_number,
    )
    time = now.strftime('%I:%M:%p')
    return render(request,'events/home.html',{
        "name":name,
        "year":year,
        "month":month,
        "month_number":month_number,
        "cal":cal,
        "current_year":current_year,
        "time":time,
        "event_list":event_list,
    })