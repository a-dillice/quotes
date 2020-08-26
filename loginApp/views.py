from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Users
import bcrypt

# index 
def index(req):

    # render login home/index page
    return render(req, "login.html")

# register 
def register(req):

    # check request
    if req.method == "POST":

        # grab post
        postData = req.POST

        # check validation
        errors = Users.objects.validateRegistration(postData)        

        # FAIL: we have errors
        if len(errors) > 0:

            # loop thru and store in messages
            for v in errors.values():
                messages.error(req, v, extra_tags='registration')
            
            # return redirect home
            # return render(req, "login.html", errors)
            return redirect("loginApp:home")

        # SUCCESS: go to quotes page
        else:

            # init
            fname = postData['reg-fname'].strip()
            lname = postData['reg-lname'].strip()
            email = postData['reg-email'].strip()
            
            # encrypt password
            password = bcrypt.hashpw(postData['reg-password'].strip().encode(), bcrypt.gensalt()).decode()

            # save user
            newUser = Users.objects.create(firstName=fname, lastName=lname, email=email, password=password)
            
            # create login session
            req.session['loggedin'] = newUser.id

            # go to quotes page
            return redirect('quoteApp:quotes') 


    # FAIL: if POST fails go back to home 
    return redirect('loginApp:home')

# login 
def login(req):

    # check request
    if req.method == "POST":

        # grab post
        postData = req.POST

        # check validation
        errors = Users.objects.validateLogin(postData)

        # FAIL: we have errors
        if len(errors) > 0:

            # loop thru and store in messages
            for v in errors.values():
                messages.error(req, v, extra_tags='login')
            
            # return back 
            redirect('loginApp:home')

        # SUCCESS: go to account page
        else:
            
            # init
            email = postData['log-email'].strip()

            # check if email exists in the db
            user = Users.objects.filter(email__iexact=email)

            # query came back with something
            if user:

                # set password and user
                password = postData['log-password'].strip()
                user = user[0]
                
                # check given password
                if bcrypt.checkpw(password.encode(), user.password.encode()):

                    # create login session
                    req.session['loggedin'] = user.id

                    # return to quotes page
                    return redirect('quoteApp:quotes') 

                # FAIL: failed password check 
                else:
                    
                    # return vague err msg
                    messages.error(req, "Email and/or password was invalid.", extra_tags='login')
            
            # FAILED: email not found
            else:

                # return vague err msg
                messages.error(req, "Email and/or password was invalid.", extra_tags='login')

    # return 
    return redirect("loginApp:home")

# account
def account(req, id):

    # just check for session
    if "loggedin" in req.session and id == req.session["loggedin"]:

        # get user name
        user = Users.objects.get(id=req.session["loggedin"])

        # setup data to pass
        data = {
            'user':user
        }
        
        # SUCCESS: go to account page
        return render(req, "account.html", data)

    # FAIL: if session fails go back to home 
    return redirect('loginApp:home')

# update user account
def accountUpdate(req, id):

    # just check for session
    if "loggedin" in req.session:

        # check post method
        if req.method == "POST":
            
            # grab id
            id = req.session["loggedin"]

            # validate
            errors = Users.objects.accountUpdate(req.POST, id)

            # grab errors
            if len(errors) > 0:
                
                # loop thru and store in messages
                for v in errors.values():
                    messages.error(req, v)
            
            # update table
            else:

                # get post data
                fname = req.POST['account-fname'].strip()
                lname = req.POST['account-lname'].strip()
                email = req.POST['account-email'].strip()
                
                # get this user
                thisUser = Users.objects.get(id=id)
                
                # update thier account in table
                thisUser.firstName = fname
                thisUser.lastName = lname
                thisUser.email = email

                # save data
                thisUser.save()

                # send sucess msg
                messages.success(req, "Account was updated successfully.")

    # return to account page
    return redirect("loginApp:account", id=id)

# logout
def logout(req):

    # check method
    if req.method == "GET":

        # delete all session data
        req.session.flush()

    # whatever happend just go back home
    return redirect("loginApp:home")
