
from django import forms
from .models.Gasto import Gasto
from .models.TipoGasto import TipoGasto
from .models.MetodoPago import MetodoPago
from .models.Viaje import Viaje

class RegistrarGastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['viaje', 'fecha', 'valor_original', 'metodo_pago', 'tipo_gasto']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Selecciona la fecha'}),
            'valor_original': forms.NumberInput(attrs={'placeholder': 'Valor del gasto'}),
            'viaje': forms.Select(attrs={'placeholder': 'Selecciona el viaje'}),
            'metodo_pago': forms.Select(attrs={'placeholder': 'Método de pago'}),
            'tipo_gasto': forms.Select(attrs={'placeholder': 'Tipo de gasto'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        viaje = cleaned_data.get('viaje')
        fecha = cleaned_data.get('fecha')

        if viaje and not viaje.esta_activo():
            self.add_error('viaje', 'No se pueden registrar gastos en un viaje que no está activo.')

        if viaje and fecha:
            if fecha < viaje.fecha_inicio or fecha > viaje.fecha_fin:
                self.add_error('fecha', 'La fecha del gasto debe estar dentro del rango del viaje.')
                
                
class RegistrarViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ['nombre','fecha_inicio', 'fecha_fin', 'presupuesto_diario', 'moneda']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del viaje o ciudad de destino'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha de inicio'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha de fin'}),
            'presupuesto_diario': forms.NumberInput(attrs={'placeholder': 'Presupuesto diario en tu moneda'}),
            'moneda': forms.TextInput(attrs={'placeholder': 'Ej: COP, USD'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            self.add_error('fecha_fin', 'La fecha de fin debe ser igual o posterior a la fecha de inicio.')