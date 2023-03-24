from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from mainbox.models import customer

# Create your views here.
def login(request):  
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
                username= request.POST['username']
                password= request.POST['password']
                
                user= auth.authenticate(username= username, password= password)

                if user is not None:
                    auth.login(request, user)
                    return redirect('/')
                
                else:
                    messages.info(request, 'Invalid credentials')
                    return render(request, 'auth/login.html')
        else:
            return render(request, 'auth/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
                username = request.POST['name']
                email= request.POST['email']
                password= request.POST["password"]
                con_password= request.POST['confirm-password']

                
                if password == con_password:
                    if User.objects.filter(email=email).exists():
                        messages.info(request, 'Email already taken.')
                        return render(request, 'auth/register.html')
                    elif User.objects.filter(username= username).exists():
                        messages.info(request, 'Username already taken.')
                        return render(request, 'auth/register.html')

                    else:
                        user= User.objects.create_user(username= username, email= email, password= password)
                        user.save();

                        user_login= auth.authenticate(username= username, password= password)
                        auth.login(request,  user_login)
                        
                        user_model = User.objects.get(username = username)
                        new_customer = customer.objects.create(user= user_model, name= user_model.username, email= user_model.email)
                        new_customer.save();
                        return redirect('/')
                else:
                    messages.info(request, 'Passwords not matching.')
                    return render('auth/register')
        else:
            return render(request, 'auth/register.html')  

@login_required(login_url='/register')
def logout(request):
        auth.logout(request)
        return redirect('/')