from django.db import models
from datetime import datetime, timedelta
import re


class UserManager(models.Manager):
    def basic_validator(self, data):        #data
        errors = {}         #errors dictionary

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #for email

        if len(data['first_name']) <1:                                      #validations
            errors['first_name'] = 'Please enter your first name!'

        if len(data['last_name']) <1:
            errors['last_name'] = 'Please enter your last name!'

        if len(data['email']) <1:
            errors['email'] = 'Please enter your email!'

        elif not EMAIL_REGEX.match(data['email']):                  #else if for email
            errors['email'] = 'Please enter a valid email address!'

        if len(data['password'])< 8:
            errors['password'] = 'Please enter at least 8 characters for your password!'

        if data['pw_confirm'] != data['password']:
            errors['pw_confirm'] = 'Please match your password to its confirmation!'

        return errors



class TripManager(models.Manager): ####### MANAGER NOT MODEL ####             #for the class trip validations
    def basic_validator(self, data):
        errors = {}


        if len(data['destination']) <3:
            errors['destination'] = 'Please enter a valid destination of at least 3 characters'

        if len(data['start_date']) <4:
            errors['start_date'] = 'Please enter a start date!'

        if len(data['end_date']) <4:
            errors['end_date'] = 'Please enter an end date!'

       



        if len(data['plan']) <3:
            errors['plan'] = 'A plan must be provided of at least 3 characters!'        
        

        return errors


class User(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()


class Trip(models.Model):
    
    destination=models.CharField(max_length=100)
    start_date=models.DateField()
    end_date=models.DateField()
    plan=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    user=models.ForeignKey(User, on_delete=models.CASCADE) #1 user has many trips
    objects=TripManager()