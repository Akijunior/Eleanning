import mimetypes

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from simplemooc.courses.models import Enrollment
from .forms import RegisterForm, EditAccountForm



def download_file(request):
    # fill these variables with real values
    fl_path = '/file/path'
    filename = 'downloaded_file_name.extension'

    fl = open(fl_path, 'r')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


@login_required  # Só permite acessa se estiver logado, não sendo possivel acessar diretamente pela url
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    enrollments = Enrollment.objects.filter(user=request.user)
    context = {'enrollments': enrollments, }
    return render(request, template_name, context)


@login_required  # Só permite acessa se estiver logado, não sendo possivel acessar diretamente pela url
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        # Pegando a instancia que está sendo alterada (model atual)
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance=request.user)
            # context['success']=True # Apenas como feedback
            messages.success(request, 'Os dados da sua conta foram atualizados com sucesso')
            return redirect('accounts:dashboard')
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)


# Form usado como base
def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Retorna um usuário

            # Ao se cadastrar será efetuado o login do usuário
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )
            # Fazendo autenticação
            login(request, user)
            return redirect('core:home')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)
