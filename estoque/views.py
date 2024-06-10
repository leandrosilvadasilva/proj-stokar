from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Alimento
from .forms import AlimentoForm
from django.utils import timezone
from django.shortcuts import render

class AlimentoBaseView:
    def form_valid(self, form):
        nome = form.cleaned_data['nome']
        validade = form.cleaned_data['validade']
        peso = form.cleaned_data['peso']

        # Verifica se a data de validade é posterior à data atual
        if validade < timezone.now().date():
            return render(self.request, 'estoque/alimento_error_date.html')

        # Busca se o alimento já existe no estoque
        alimento_existente = Alimento.objects.filter(
            Q(nome__iexact=nome),
            Q(validade=validade),
            Q(peso=peso)
        ).first()

        if alimento_existente:
            # Incrementa a quantidade do alimento existente com a quantidade do formulário
            alimento_existente.quantidade += form.cleaned_data['quantidade']
            alimento_existente.save()

            # Se não achar, redireciona para a lista de alimentos, caso contrário, exclui a entrada que está sendo atualizada
            if isinstance(self, CreateView):
                return redirect('alimento_list')
            else:
                self.object.delete()
                return redirect('alimento_list')

        # Caso o alimento não for encontrado, chama o método form_valid da classe pai
        return super().form_valid(form)

class AlimentoListView(ListView):
    model = Alimento
    template_name = 'estoque/alimento_list.html'


class AlimentoCreateView(CreateView):
    model = Alimento
    form_class = AlimentoForm 
    template_name = 'estoque/alimento_create.html'
    success_url = reverse_lazy('alimento_list')

class AlimentoUpdateView(AlimentoBaseView, UpdateView):
    model = Alimento
    template_name = 'estoque/alimento_update.html'
    form_class = AlimentoForm
    success_url = reverse_lazy('alimento_list')

class AlimentoDeleteView(DeleteView):
    model = Alimento
    template_name = 'estoque/alimento_delete.html'
    success_url = reverse_lazy('alimento_list')
