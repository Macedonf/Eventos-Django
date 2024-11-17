from django import forms
from events.models import Participante


class ParticipanteForm(forms.ModelForm):
    INGRESSO_CHOICES = [
        ('PAGO', 'Pago'),
        ('NAO_PAGO', 'Não Pago'),
    ]

    ingresso = forms.ChoiceField(
        choices=INGRESSO_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Participante
        fields = ['nome', 'email', 'evento_associado', 'ingresso', 'valor_ingresso']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite o email'}),
            'data_inscricao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'evento_associado': forms.Select(attrs={'class': 'form-control', 'maxlength': 10}),
            'valor_ingresso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o valor do ingresso'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        evento_associado = cleaned_data.get("evento_associado")

        if email and evento_associado:
            if Participante.objects.filter(email=email, evento_associado=evento_associado).exists():
                raise forms.ValidationError("Este e-mail já está cadastrado para este evento.")

        return cleaned_data