from django.shortcuts import render, redirect
from django.contrib import messages, auth
# Create your views here.
from django.contrib.auth.models import User
from contacts.models import Contact

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # check duplicate check for username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Duplicate Username')
            return redirect('register')
        # Email check
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Duplicate Email')
            return redirect('register')

        user = User.objects.create_user(username=username,password=password,email=email,
                                        first_name=first_name,last_name=last_name)
        # Login after register
        # auth.login(request, user)
        # messages.success(request, "You are now logged in")
        # return redirect('index')

        user.save()
        messages.success(request, 'You are now logged in')
        return redirect('login')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('dashboard')
        else:
            messages.error(request, 'Login failed')
            return redirect("login")
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are logged out')
        return redirect('index')
    else:
        messages.success(request, 'Unabled to log out')
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)