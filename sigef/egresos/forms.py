from django import forms
from django.forms import inlineformset_factory, BaseFormSet

from sigef.egresos.models import Factura, Proveedor, Concepto


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'


class ConceptoForm(forms.ModelForm):
    class Meta:
        model = Concepto
        fields = '__all__'
