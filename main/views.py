from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *
import bcrypt

# Create your views here.
def display_login_and_register_page(request): #displaying page for login/register // url will be ''
    return render(request, 'index.html')    #creating the html page // 2 forms

def create_user(request):                               #url will be path(/create)
    errors = User.objects.basic_validator(request.POST)     #validations

    if len(errors) > 0:                   #this is for the validations // if there is more than 1 error you will be redirected to the same page and try again
        for key, err in errors.items():
            messages.error(request, err)
        return redirect('/')


    hashed_pw = bcrypt.hashpw(              #to hash the password
        request.POST['password'].encode(),
        bcrypt.gensalt()
    ).decode()

    created_user = User.objects.create(         #creating the user // attributes 
        first_name= request.POST['first_name'], #orange has to match models
        last_name= request.POST['last_name'],   #yellow has to match name inside of html
        email= request.POST['email'],
        password = hashed_pw,
    )

    request.session['user_id'] = created_user.id        #saving the user id to session // will refer to this later
    return redirect('/dashboard')

def login(request):
    potential_users = User.objects.filter(email=request.POST['email']) #email if not just change to username
    if len(potential_users) == 0:
        messages.error(request,"Email is not in our system")    #checking validations
        return redirect('/')                                #will redirect you to the same page
    user = potential_users[0]                               #first user

    if not bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
        messages.error(request, "Please check your email and password")


        return redirect('/')
    
    request.session['user_id'] = user.id    #ADD THE REQUEST.SESSION FROM ABOVE
    return redirect('/dashboard') 




############################# ABOVE IS THE LOGIN AND REG PAGE ######################

############ BELOW DASHBOARD PAGE ############

def display_dashboard_page(request):  
    if "user_id" not in request.session:
        messages.error(request, "You must be logged in to view that page.") 
        return redirect("/")                         #will have to take in all trips // have to get a specific user which comes from the session
    


    context= {
        "trips":Trip.objects.all(), #COMMA!!
        "user":User.objects.get(id=request.session["user_id"])
    }
    
    return render(request, "dashboard_page.html",context)

############ CREATING TRIP BELOW ############

def create_trip_page(request):       #have its own webpage url /trips/new         #just the page passing all specific users
    context = {
        
        "user":User.objects.get(id=request.session["user_id"]) #using session 
    }

    return render(request, "create_trip_page.html", context) #create the html page


def create_trip_action(request):
    errors=Trip.objects.basic_validator(request.POST)


    if len(errors) >0:
        for err in errors.values():
            messages.error(request, err)
        return redirect("/trips/new") #UPDATE THE REDIRECT WITH EVERY FUNCTIONS VALIDATIONS #
    

    Trip.objects.create(
        destination=request.POST["destination"],
        start_date=request.POST["start_date"],
        end_date=request.POST["end_date"],
        plan=request.POST["plan"],
        user = User.objects.get(id=request.session['user_id']) #need to include to make the connection
    )

    return redirect("/dashboard")


def edit_trip_page(request, trip_id): #id to know which trip
    trip=Trip.objects.get(id=trip_id)                  #creating a variable
    trip.start_date=trip.start_date.strftime("%Y-%m-%d") 
    trip.end_date=trip.end_date.strftime("%Y-%m-%d")

    context={
        "trip": trip, #refering to the variable
        "user":User.objects.get(id=request.session["user_id"]) #including session user id // we need a specific user
    }
    return render(request, "edit_page.html", context)


def edit_trip_action(request, trip_id):
    errors=Trip.objects.basic_validator(request.POST)        #validations

    if len(errors) >0:
        for err in errors.values():
            messages.error(request, err)
        return redirect(f"/trips/edit/{trip_id}")     #f string bc he need the trip id inside the url 
    

    newtrip=Trip.objects.get(id=trip_id)           #creating a variable

    newtrip.destination=request.POST["destination"]                  #refering to the new variable
    newtrip.start_date=request.POST["start_date"]
    newtrip.end_date=request.POST["end_date"]
    newtrip.plan=request.POST["plan"]

    newtrip.save() ##### DONT FORGET TO SAVE ########################################

    return redirect("/dashboard")


######## EDIT TRIP PAGE AND EDIT ACTION PAGE ABOVE #######
######## BELOW IS THE VIEW TRIP DECRIPTION PAGE######

def view_trip_page(request, trip_id):
    context={
        "trip": Trip.objects.get(id=trip_id),
        "user": User.objects.get(id=request.session["user_id"])
    }
    return render(request, "view_trip_page.html", context)


def logout(request):
    request.session.pop("user_id")

    return redirect('/')




def delete(request, trip_id):                #deleting the specific trip
    trip=Trip.objects.get(id=trip_id)
    trip.delete()                        #dont forget

    return redirect("/dashboard")  


