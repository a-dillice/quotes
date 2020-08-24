from django.shortcuts import render, redirect, HttpResponse
from .models import Users, Quotes, Likes
from django.contrib import messages

# all quotes page
def quotes(req):

    # just check for session
    if "loggedin" in req.session:

        # grab users
        user = Users.objects.get(id=req.session['loggedin'])

        # get all quotes
        allQuotes = Quotes.objects.all()

        # data
        data = {
            "allQuotes":allQuotes,
            "user":user
        }

        # redirect to login
        return render(req, "quotes.html", data)  

    # FAILED: not logged in
    else:

        # redirect to login
        return redirect("loginApp:home")    

# process adding quote to table
def addQuotes(req):
    
    # just check for session
    if "loggedin" in req.session:

        # if we have post
        if req.method == "POST":
            
            # get post
            postData = req.POST

            # get user id
            id = req.session['loggedin']

            # validate
            errors = Quotes.objects.validateQuote(postData)

            # grab errors
            if len(errors) > 0:
                
                # loop thru and store in messages
                for v in errors.values():
                    messages.error(req, v)

            # SUCCESS: add quote to table
            else:
                
                # show success meg
                messages.success(req, "Quote added successfully.")

                # grab data we need
                user = Users.objects.get(id=id)
                author = postData['add-author'].strip()
                quote = postData['add-quote'].strip()

                # update table/obj
                Quotes.objects.create(user=user, author=author, quote=quote)

        # return redirect
        return redirect("quoteApp:quotes")

    # FAILED: not logged in
    else:

        # redirect to login
        return redirect("loginApp:home")

# delete quotes
def deleteQuotes(req, id):

    # just check for session
    if "loggedin" in req.session:

        # if we have post
        if req.method == "POST":

            # delete quote
            delQuote = Quotes.objects.get(id=id)
            delQuote.delete()

        # return redirect
        return redirect("quoteApp:quotes")

    # FAILED: not logged in
    else:

        # redirect to login
        return redirect("loginApp:home")

# like quotes
def likeQuotes(req, id):

    # just check for session
    if "loggedin" in req.session:

        # if we have post
        if req.method == "POST":
            
            # set user id
            userID = req.session['loggedin']

            # grab current user and quote
            quote = Quotes.objects.get(id=id)
            user  = Users.objects.get(id=userID)
            liked = Likes.objects.filter(user_id = userID, quotes_id=id)
            
            # if we havent liked it already
            if len(liked) <= 0:
                
                # add the user and quote to the like
                Likes.objects.create(user=user, quotes=quote)

        # return redirect
        return redirect("quoteApp:quotes")

    # FAILED: not logged in
    else:

        # redirect to login
        return redirect("loginApp:home")

# only show user quotes
def userQuotes(req, id):

    # just check for session
    if "loggedin" in req.session:

        # grab users
        user = Users.objects.get(id=req.session['loggedin'])

        # get all quotes
        allQuotes = Quotes.objects.filter(user=id)
        print(allQuotes[0].user.firstName)
        # data
        data = {
            "allQuotes":allQuotes,
            "user":user
        }

        # redirect to login
        return render(req, "my-quotes.html", data)  

    # FAILED: not logged in
    else:

        # redirect to login
        return redirect("loginApp:home")



