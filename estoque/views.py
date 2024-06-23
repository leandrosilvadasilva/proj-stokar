from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from .models import Alimento, RegistroEntrada, RegistroSaida
from django.urls import reverse_lazy
from .forms import AlimentoForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

#Gerar PDF 
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

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

    def form_valid(self, form):
        # Salva o alimento
        alimento = form.save()

        # Registra a entrada do alimento
        registro_entrada = RegistroEntrada(alimento=alimento, quantidade=alimento.quantidade)
        registro_entrada.save()

        return super().form_valid(form)
    
class UtilizarAlimentoView(View):
    def post(self, request, pk):
        alimento = get_object_or_404(Alimento, pk=pk)
        quantidade_utilizada = int(request.POST.get('quantidade', 0))

        if quantidade_utilizada > 0 and quantidade_utilizada <= alimento.quantidade:
            # Reduz a quantidade disponível do alimento
            alimento.quantidade -= quantidade_utilizada
            alimento.save()

            # Registra a saída do alimento utilizado
            registro_saida = RegistroSaida(alimento=alimento, quantidade=quantidade_utilizada, data_registro=timezone.now())
            registro_saida.save()

        return redirect('alimento_list')

class AlimentoUpdateView(UpdateView):
    model = Alimento
    template_name = 'estoque/alimento_update.html'
    form_class = AlimentoForm
    success_url = reverse_lazy('alimento_list')

    def form_valid(self, form):
        alimento = form.save(commit=False)
        if form.cleaned_data['quantidade'] > 0:
            registro_entrada = RegistroEntrada(alimento=alimento, quantidade=form.cleaned_data['quantidade'])
            registro_entrada.save()
        return super().form_valid(form)

class AlimentoDeleteView(DeleteView):
    model = Alimento
    template_name = 'estoque/alimento_delete.html'
    success_url = reverse_lazy('alimento_list')


class EntradasListView(ListView):
    model = RegistroEntrada
    template_name = 'estoque/entradas_list.html'
    context_object_name = 'entradas'

    def get_queryset(self):
        return RegistroEntrada.objects.all().order_by('-data_registro')

class SaidasListView(ListView):
    model = RegistroSaida
    template_name = 'estoque/saidas_list.html'
    context_object_name = 'saidas'

    def get_queryset(self):
        return RegistroSaida.objects.all().order_by('-data_registro')


class EntradasPDFView(View):
    def get(self, request):
        entradas = RegistroEntrada.objects.all()  # obtém todas as entradas

        template_path = 'estoque/entradas_pdf.html'
        context = {'entradas': entradas}
        
        # Renderiza o template
        template = get_template(template_path)
        html = template.render(context)

        # Cria o PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="entradas.pdf"'

        # Converte HTML para PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Ocorreu um erro ao gerar o PDF.')

        return response

class SaidasPDFView(View):
    def get(self, request):
        saidas = RegistroSaida.objects.all()  # obtém todas as saídas

        template_path = 'estoque/saidas_pdf.html'
        context = {'saidas': saidas}
        
        # Renderiza o template
        template = get_template(template_path)
        html = template.render(context)

        # Cria o PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="saidas.pdf"'

        # Converte HTML para PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Ocorreu um erro ao gerar o PDF.')

        return response