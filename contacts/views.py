from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

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

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id = listing_id, user_id = user_id)
            if has_contacted: 
                messages.error(request, ' you have already made an inquiry for this listing')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing = listing, listing_id = listing_id, name = name, email = email,
                          phone = phone, message = message, user_id = user_id)
        
        contact.save()

        #send mail
        send_mail(
            'Property listing inquiry',
            'There has been an inquiry for ' + listing + '. sign into the admin panel for more info',
            'jacksnikkers@gmail.com',
            [realtor_email, 'arianazvp@gmail.com'],
            fail_silently=False
        )

        messages.success(request, "your request  has been submitted, a realtor will get back to you soon")

        return redirect('/listings/' + listing_id)