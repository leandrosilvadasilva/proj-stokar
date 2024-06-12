from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import login, logout, Authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


class HomeView(TemplateView):
    template_name = 'autenticacao/home.html'


class SigupView(TemplateView):
    template_name = 'autenticacao/sigup.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            return render(request, self.template_name, {'error_message': 'Usuário já existe.'})

        # Verifica se as senhas são iguais
        if password1 != password2:
            return render(request, self.template_name, {'error_message': 'As senhas não coincidem.'})

        # Se chegou até aqui, cria o usuário
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # Redireciona para a página 'home.html' após o cadastro bem-sucedido, DEVERÁ REDIRECIONAR PARA A LISTA.
        return redirect('home')


class SiginView(TemplateView):
    template_name = 'autenticacao/sigin.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autenticar o usuário
        user = authenticate(username=username, password=password)

        if user is not None:
            # Login bem-sucedido, redireciona para a página inicial
            login(request, user)
            # REDIRECIONAR PARA PAGINA
            return redirect('/estoque') 
        else:
            # Exibir mensagem de erro se o login falhar
            messages.error(request, 'Nome de usuário ou senha inválidos.')
            return redirect('sigin')

class ExitView(TemplateView):
    template_name = 'autenticacao/exit.html'

    def post(self, request, *args, **kwargs):
        # Realiza o logout do usuário
        logout(request)
        # Redireciona para a página inicial após o logout
        return redirect('home')
