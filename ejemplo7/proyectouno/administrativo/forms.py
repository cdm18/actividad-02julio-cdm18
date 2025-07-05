from django.forms import ModelForm
from django import forms

from administrativo.models import *

class MatriculaForm(ModelForm):
    class Meta:
        model = Matricula
        fields = ['estudiante', 'modulo', 'comentario', 'costo']



class MatriculaEditForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MatriculaEditForm, self).__init__(*args, **kwargs)
        self.initial['estudiante'] = self.instance.estudiante
        self.fields["estudiante"].widget = forms.widgets.HiddenInput()
        self.initial['modulo'] = self.instance.modulo
        self.fields["modulo"].widget = forms.widgets.HiddenInput()
        self.fields["costo"].widget = forms.HiddenInput()

    class Meta:
        model = Matricula
        fields = ['estudiante', 'modulo', 'comentario', 'costo']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'placeholder': 'Escribe aquí tu comentario...'
            }),}

class EstudianteForm(ModelForm):
    class Meta:
        model = Estudiante
        # No incluimos 'modulos' porque es M2M a través de Matricula
        fields = ["nombre", "apellido", "cedula", "edad", "tipo_estudiante"]
        widgets = {
            "tipo_estudiante": forms.Select(
                attrs={"class": "form-control"}
            ),
        }

    # Validaciones básicas
    def clean_cedula(self):
        cedula = self.cleaned_data["cedula"]
        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError("Ingrese una cédula válida de 10 dígitos.")
        return cedula

    def clean_edad(self):
        edad = self.cleaned_data["edad"]
        if edad <= 0:
            raise forms.ValidationError("La edad debe ser un número positivo.")
        return edad


class EstudianteEditForm(EstudianteForm):
    """
    Permite editar todos los datos excepto la cédula, que se mantiene fija.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos la cédula de solo lectura/oculta
        self.fields["cedula"].widget = forms.widgets.HiddenInput()


class ModuloForm(ModelForm):
    class Meta:
        model = Modulo
        fields = ["nombre"]  # Solo un campo, tiene un select con las opciones


class ModuloEditForm(ModuloForm):
    """Para este ejemplo no necesitamos lógica extra, heredamos tal cual."""
    pass