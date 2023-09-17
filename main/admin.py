from django.contrib import admin
from main.models import Department, Post, Doctor, Patient, Appointment, Time, Feedback


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'post')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'blood_type', 'gender', 'discount_status')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'doctor', 'status', 'owner')


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = ('time',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('text', 'owner')
