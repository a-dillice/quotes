from django.db import models
from datetime import datetime
import re

# validation class
class Validator(models.Manager):
    
    # login validator
    def validateRegistration(self, postData):

        # init
        errors = {}
              
        # if we recieved any post data
        if postData:

            # init
            passLimit = 8
            fnameLimit = 2
            lnameLimit = 2
            ageLimit = 13
            emailRegEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            fname = postData['reg-fname'].strip()
            lname = postData['reg-lname'].strip()
            email = postData['reg-email'].strip()
            password = postData['reg-password'].strip()
            confirmPassword = postData['reg-password-confirm'].strip()
            bday = postData['reg-bday'].strip()

            # first name check
            if len(fname) < fnameLimit:
                
                # record err
                errors['firstName'] = f"First name needs to have at least {fnameLimit} characters."
            
            # last name check
            if len(lname) < lnameLimit:
                
                # record err
                errors['lastName'] = f"Last name needs to have at least {lnameLimit} characters."
            
            # email match check - 
            if not emailRegEx.match(email):

                # record err
                errors['email'] = "Email is not valid."

            # if valid then check if unique
            else:

                # grab all emails in user table/obj
                allEmails = Users.objects.filter(email__iexact=email)
                
                # we have duplicate email
                if len(allEmails) > 0:
                    
                    # record err
                    errors['email'] = "That email has been taken."

            # password check
            if len(password) < passLimit:

                # record err
                errors['password'] = f"Password needs to be {passLimit} characters long."
            
            # pass confirm check
            if password != confirmPassword:

                # record err
                errors['confirm'] = "Passwords did not match."

            # # bday check 
            if bday != "":

                # try/except because user can provide bad date format
                try:

                    # init
                    age = datetime.strptime(bday, "%B %d, %Y")      #convert given date from str
                    today = datetime.now()                          #grab todays date
                    diff = int((today - age).days/365)              #get the years between today and the given bday

                    # make sure we are over the age limit
                    if diff < ageLimit:

                        # record error
                        errors["underAge"] = "You are not old enough to register." 

                # catch error
                except ValueError:

                    # record error
                    errors["underAge"] = "The date provided was not in the correct format."

            # required bday
            else:

                # record error
                errors["birthday"] = "A date of birth is required."          

        # error
        else:

            errors['noData'] = "No form data was given."
        
        # age check
        return errors

    # login validator
    def validateLogin(self, postData):

        # init
        errors = {}
              
        # if we recieved any post data
        if postData:

            # grab post data
            email = postData['log-email'].strip()
            password = postData['log-password'].strip()
            
            # check if email was given 
            if len(email) < 1:

                # return error
                errors['logEmail'] = "Please provide an email."

            # check if password was given 
            if len(password) < 1:

                # return error
                errors['logPassword'] = "Please provide a password."

        # error
        else:

            # return err
            errors['noData'] = "No form data was given."
        
        # age check
        return errors

    # update account info
    def accountUpdate(self, postData, userId):

        # init
        errors = {}
        print(postData)              
        # if we recieved any post data
        if postData:

            # init
            fnameLimit = 2
            lnameLimit = 2            
            emailRegEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            fname = postData['account-fname'].strip()
            lname = postData['account-lname'].strip()
            email = postData['account-email'].strip()

            # first name check
            if len(fname) < fnameLimit:
                
                # record err
                errors['firstName'] = f"First name needs to have at least {fnameLimit} characters."
            
            # last name check
            if len(lname) < lnameLimit:
                
                # record err
                errors['lastName'] = f"Last name needs to have at least {lnameLimit} characters."
            
            # email match check - 
            if not emailRegEx.match(email):

                # record err
                errors['email'] = "Email is not valid."

            # if valid then check if unique
            else:

                # exclude our current user and then grab all emails in user table/obj
                allEmails = Users.objects.exclude(id=userId)
                allEmails = allEmails.filter(email__iexact=email)

                # we have duplicate email
                if len(allEmails) > 0:
                    
                    # record err
                    errors['email'] = "That email has been taken."

        # error
        else:

            # no post err
            errors['noData'] = "No form data was given."

        # return errors
        return errors

# Create your models here.
class Users(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validator()

