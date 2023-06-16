from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UserPasswordChange, UserProfileForm, ChangeProfileForm, MorefeInfoUserProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from .models import UserProfile
from tasks.models import Task
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.mail import send_mail



def add_user(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Crie uma instância de User com base nos dados do formulário
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            # Crie uma instância de UserProfile associada ao usuário criado
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            # Redirecione para uma página de sucesso ou faça algo adequado
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('accounts:add_user')

    else:
        form = UserProfileForm()
    return render(request, 'tasks/accounts/add_user.html', {'form': form})
'''
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
            return redirect('accounts:login')

    else:
        return render(request, 'tasks/accounts/login.html', context)
'''

def logout_user(request):   
    logout(request)
    return redirect('core:home')


@login_required(login_url="/login")
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordChange(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso.')
            return redirect('accounts:change_password')
        else:
            messages.warning(request, 'Por favor, corrija os erros abaixo.')
    
    form = UserPasswordChange(request.user)
    return render(request, 'tasks/accounts/change_password.html', {'form': form})


@login_required(login_url="/login")
def view_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    tasks = Task.objects.filter(owner=request.user) 
    
    for task in tasks:
        task.progress = task.porcentagem_dias_passados()

    context = { 'user_profile': user_profile, 
               'tasks':tasks,}

    return render(request, 'tasks/accounts/user_profile.html', context)


@login_required(login_url="/login")
def change_user_profile(request):
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil alterado com sucesso")
            return redirect('accounts:change_profile')  # Redireciona para a página de perfil
    else:
        form = ChangeProfileForm(instance=request.user.profile)
    
    context = {'form': form}
    return render(request, 'tasks/accounts/change_profile.html', context)


@login_required(login_url="/login")
def more_info(request):
    if request.method == 'POST':          
        form = MorefeInfoUserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Informações alteradas com sucesso")
            return redirect('accounts:user_profile')
    else:
        form = MorefeInfoUserProfileForm(instance=request.user.profile)

    return render(request, 'tasks/accounts/more_info.html', {'form': form})


def recovery(request):
    if request.method == 'POST': 
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            token = default_token_generator.make_token(user)
            uid = user.id
            password_reset_url = request.build_absolute_uri(request,reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
            
            assunto = f"Recupere sua senha do TaskMinder!"
            mensagem = f"clique no link abaixo para recuperar sua senha:\n{password_reset_url}"
            # Supondo que o atributo "owner" é uma instância do modelo User que representa o responsável pela tarefa
            destinatarios = [user.email]
            remetente = "vlogsplayer10@gmail.com"

            send_mail(assunto, mensagem, remetente,
                      destinatarios, fail_silently=False)

            return redirect('accounts:password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'tasks/core/login_page.html', {'form': form})