from django.shortcuts import render, redirect 
#additional
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import User, Report
# Create your views here.

def index(request):
    reports_count =len(Report.objects.all())
    unread = Report.objects.filter(status="unread")
    unread_count = len(Report.objects.filter(status="unread"))
    pending_count = len(Report.objects.filter(status="pending"))
    solved_count = len(Report.objects.filter(status="resolved"))
    return render(request,"jedsreport/index.html",{
        "unread":unread,
        "unread_count":unread_count,
        "pending_count":pending_count,
        "solved_count":solved_count,
        "reports_count":reports_count
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "jedsreport/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "jedsreport/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "jedsreport/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "jedsreport/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "jedsreport/register.html")

#Report form
class NewReport(forms.Form):
    """ Form used to report a problem """

    #Set a list of categories
    CATEGORIES = [('LABORATORY','LABORATORY'),('OFFICE','OFFICE'),
        ('AUDIOVISUAL','AUDIOVISUAL'),('WINDOW/DOOR/TABLE/CHAIR','WINDOW/DOOR/TABLE/CHAIR'),
        ('HVAC/FIRE/PLUMBING/ELECTRICAL','HVAC/FIRE/PLUMBING/ELECTRICAL'),('COMPUTER','COMPUTER'),
        ('OTHERS','OTHERS')]
    category = forms.CharField(label="Category", widget=forms.Select(choices=CATEGORIES))
    title = forms.CharField(max_length=64, label = "Object")
    description = forms.CharField(widget = forms.Textarea, label="Description")
    venue = forms.CharField(max_length=40,label="Venue/Office/Lab name")
    image = forms.FileField(required=False)

    #Set a list of existing departments
    DEPARTMENTS = [('Civil','CIVIL'),
        ('Mechanical','MECHANICAL'),
        ('Electronics & Computer','ELECTRONICS & COMPUTER'),
        ('Electrical','ELECTRICAL'),
        ('Mining & Metallurgy','MINING & METALLURGY')]
    department = forms.CharField(label="Department", widget=forms.Select(choices=DEPARTMENTS))

#Creating and saving new reports
def new_report(request):
    if request.method =="POST":
        if request.FILES:
            form = NewReport(request.POST, request.FILES)
            if form.is_valid():
                #Get the user's details
                reporter = request.user

                #Collect data from submitted form
                title = form.cleaned_data["title"]
                description = form.cleaned_data["description"]
                venue = form.cleaned_data["venue"]
                department = form.cleaned_data["department"]
                category = form.cleaned_data["category"]
                image = request.FILES["image"]

                #Create a new Report model and save it
                this_report = Report(reporter=reporter, title=title, description=description,
                    venue = venue, department=department,category=category, image=image)
                this_report.save()

                #redirect user to home page after submitting the form
                return redirect("index")
        else:
            form = NewReport(request.POST)
            if form.is_valid():
                #Get the user's details
                reporter = request.user

                #Collect data from submitted form
                title = form.cleaned_data["title"]
                description = form.cleaned_data["description"]
                venue = form.cleaned_data["venue"]
                department = form.cleaned_data["department"]
                category = form.cleaned_data["category"]
                #image = request.FILES["image"]

                #Create a new Report model and save it
                this_report = Report(reporter=reporter, title=title, description=description,
                    venue = venue, department=department,category=category)
                this_report.save()

                #redirect user to home page after submitting the form
                return redirect("index")
    return render(request,"jedsreport/newreport.html",{
        "form": NewReport().as_p()
    })

def inactive(request):
    inactives = Report.objects.filter(solved=True)
    return render(request,"jedsreport/inactive.html",{
        "inactives":inactives
    })

def report(request,report_id):
    report_view = Report.objects.get(id=report_id)
    return render(request, "jedsreport/report.html",{
        "report_view":report_view
    })

#Set report as pending
def pending(request,report_id):
    if request.method =="POST":
        reason = request.POST["pending"]
        pending_report = Report.objects.get(id=report_id)
        pending_report.status = "pending"
        pending_report.pending_reason = reason
        pending_report.save()
        return redirect("index")

#Display pending Items
def pending_report(request):
    pending_reports = Report.objects.filter(status="pending")
    return render(request,"jedsreport/pending.html",{
        "pending_reports":pending_reports 
    })

import matplotlib.pyplot as plt
import io
import urllib,base64
import numpy as np
import matplotlib
matplotlib.use ('Agg')   #Important to add this

def plot(request):
    # Initialize departments
    departments = []
    #Get all existing departments
    for department in Report.objects.all():
        departments.append(department.department)
    #Get rid of duplicates
    departments = set(departments)
    #Get remaining list
    departments = list(departments)

    #Get corresponding counts of reports
    report_count = []
    for department in departments:
        count = len(Report.objects.filter(department=department))
        report_count.append(count)
    
    #Now plot using departments and corresponding values
    y_pos = np.arange(len(departments))
    
    # Create bars
    plt.bar(y_pos, report_count)
    
    # Create names on the x-axis
    plt.xticks(y_pos, departments)
    plt.title("Number of reports by Departments")
    plt.ylabel("Number of reports")

    #plt.plot(range(10))
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string= base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request,'jedsreport/plot.html',{
        "data":uri
    })


#Solved function to mark report as solved
def solved(request,report_id):
    if request.method == "POST":
        item = Report.objects.get(id=report_id)
        item.solved = True
        item.save()
        return redirect("index")
        