
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Alimento
from .forms import AlimentoForm

class AlimentoListView(ListView):
    model = Alimento
    template_name = 'alimento_list.html'


class AlimentoCreateView(CreateView):
    model = Alimento
    form_class = AlimentoForm  # Utilizando o formulário personalizado AlimentoForm
    template_name = 'alimento_create.html'
    success_url = reverse_lazy('alimento_list')

class AlimentoUpdateView(UpdateView):
    model = Alimento
    template_name = 'alimento_update.html'
    fields = ['nome', 'quantidade', 'validade', 'peso']
    success_url = reverse_lazy('alimento_list')

class AlimentoDeleteView(DeleteView):
    model = Alimento
    template_name = 'alimento_delete.html'
    success_url = reverse_lazy('alimento_list')
