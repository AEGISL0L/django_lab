from django import forms
from django.utils import timezone
import random
import string

from .models import FormulaRequest


def generate_petition_id(prefix: str = 'FRM') -> str:
    timestamp = timezone.now().strftime('%Y%m%d%H%M')
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f'{prefix}-{timestamp}-{random_suffix}'


class FormulaRequestCreateForm(forms.ModelForm):
    petition_id = forms.CharField(label='ID Petición', required=False, disabled=True)
    requiere_rele = forms.BooleanField(label='¿Requiere RELE?', required=False)

    class Meta:
        model = FormulaRequest
        fields = [
            'petition_id',
            'nombre',
            'descripcion',
            'requiere_rele',
            'telefono_contacto',
            'foto_receta',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_receta': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'requiere_rele': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bootstrap class para el campo disabled también
        self.fields['petition_id'].widget.attrs.update({'class': 'form-control'})

        if not self.initial.get('petition_id') and not self.data.get('petition_id'):
            self.initial['petition_id'] = generate_petition_id()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.petition_id:
            instance.petition_id = generate_petition_id()
        if commit:
            instance.save()
        return instance
