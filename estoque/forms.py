
from django import forms
from .models import Alimento

class AlimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = ['nome', 'quantidade', 'validade', 'peso']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do alimento'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantidade'}),
            'validade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso em Kg'}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '')
        return nome.title()
