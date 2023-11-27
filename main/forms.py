from django import forms
from django.core.exceptions import ValidationError

from main.models import Patient, Appointment, Feedback
from services.forms import FormStyleMixin


class PatientForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('__all__')


class AppointmentForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('date', 'time', 'doctor')

    def clean_doctor(self):
        date = self.cleaned_data['date']
        time = self.cleaned_data['time']
        doctor = self.cleaned_data['doctor']
        doctor_bd = \
            Appointment.objects.filter(doctor=doctor)\
            & Appointment.objects.filter(date=date)\
            & Appointment.objects.filter(time=time)
        if doctor_bd:
            raise ValidationError(
                'Извините, запись на данное время уже существует!'
            )

        return doctor


class FeedbackForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('text',)
