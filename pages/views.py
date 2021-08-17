from django.shortcuts import render
from django.http import HttpResponse

from listings.models import Listing
from realtors.models import Realtor
from listings.choices import bedroom_choices, price_choices, state_choices

# Create your views here.
def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    listings = listings[3:]

    context = {
        'listings' : listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices
    }
    return render(request, 'pages/index.html', context)

def about(request):
    realtors = Realtor.objects.all()
    # Get mvp
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)[0]
    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }
    return render(request, 'pages/about.html', context)