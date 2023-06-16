from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_user(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #messages.success(request, ("Login feito com sucesso!"))
            login(request, user)
            return redirect('core:home')
                
        else:
            messages.error(request, ("Erro ao tentar o login! Tente de novo."))
            return redirect('core:home_login')

    else:
        return render(request, 'tasks/core/login_page.html', context)


@login_required(login_url="/login")
def home(request):
    return render(request, 'tasks/core/landing_page/index.html', {})


