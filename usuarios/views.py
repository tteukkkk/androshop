from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})


@login_required
def perfil(request):
    usuario = request.user
    return render(request, 'usuarios/perfil.html', {'usuario': usuario})
