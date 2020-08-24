from django.db import models
from loginApp.models import Users

class Validator(models.Manager):
    
    # add quote validation
    def validateQuote(self, postData):

        # init
        errors = {}
              
        # if we recieved any post data
        if postData:
            
            # init
            authorLimit = 3
            quoteLimit = 10
            author = postData['add-author'].strip()
            quote = postData['add-quote'].strip()


            # first author check
            if len(author) < authorLimit:
                
                # record err
                errors['author'] = f"Author name needs to have at least {authorLimit} characters."
            
            # quote check
            if len(quote) < quoteLimit:
                
                # record err
                errors['quote'] = f"The quote needs to have at least {quoteLimit} characters."


        # error
        else:

            # pass err
            errors['noData'] = "No form data was given."
        
        # age check
        return errors


# quotes
class Quotes(models.Model):
    user = models.ForeignKey(Users, related_name="quotes", on_delete=models.CASCADE)
    quote = models.TextField(null=False, blank=False)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Validator()

# likes
class Likes(models.Model):
    user = models.ForeignKey(Users, related_name="likes", on_delete=models.CASCADE)
    quotes = models.ForeignKey(Quotes, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

