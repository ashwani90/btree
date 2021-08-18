from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check if user has made enquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made the enquiry')


        contact = Contact(listing=listing, listing_id=listing_id, name=name,email=email, phone=phone,
                          message=message, user_id=user_id)
        contact.save()
        # Send email
        send_mail(
            'Prpoerty enquiry',
            'There has been an inquiry for '+ listing + '. Sign in into admin panel for respond.',
            'username',
            ['email_to_send_to'],
            fail_silently=False
        )
        messages.success(request, 'Your request has been saved')
        return redirect('listings/'+listing_id)
    return render()