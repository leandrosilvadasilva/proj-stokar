
from django import forms
from .models import Alimento

class AlimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = ['nome', 'quantidade', 'validade', 'peso']
        widgets = {
            'validade': forms.DateInput(attrs={'type': 'date'}),
        }

    #Define formatação padrão de que cada palavra contida no nome deve iniciar com maiúscula; auxilia na integridade
    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '')
        return nome.title()