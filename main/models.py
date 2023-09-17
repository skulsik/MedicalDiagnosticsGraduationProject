from django.db import models
from config import settings
from services.utils import NULLABLE


class Department(models.Model):
    """ Модель отделения клиники (гинекология) """
    name = models.CharField(max_length=150, verbose_name='Название отделения (например кардиология)')

    def __str__(self):
        return f'Отдел: {self.name}'

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class Post(models.Model):
    """ Модель должности (санитар) """
    name = models.CharField(max_length=150, verbose_name='Должность (например акушер)')
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name='Отдел которому принадлежит должность'
    )

    def __str__(self):
        return f'Должность: {self.name}. {self.department}'

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Doctor(models.Model):
    """ Модель сущности доктора """
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Должность'
    )
    education = models.CharField(max_length=255, verbose_name='Образование', **NULLABLE)
    awards = models.CharField(max_length=255, verbose_name='Награды', **NULLABLE)
    experience = models.DateField(verbose_name='Стаж с "дата"', **NULLABLE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name='Владелец'
    )
    status_appointment = models.BooleanField(
        default=True,
        verbose_name='Статус врача, True - можно записаться на прем',
        **NULLABLE
    )

    def __str__(self):
        return f'{self.post}'

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'


class BloodType(models.TextChoices):
    """ Группа крови """
    ONE_NEGATIVE = 'O(|) Rh-'
    ONE_POSITIVE = 'O(|) Rh+'
    TWO_NEGATIVE = 'A(||) Rh-'
    TWO_POSITIVE = 'A(||) Rh+'
    THREE_NEGATIVE = 'B(|||) Rh-'
    THREE_POSITIVE = 'B(|||) Rh+'
    FOUR_NEGATIVE = 'AB(|V) Rh-'
    FOUR_POSITIVE = 'AB(|V) Rh+'


class GenderChoice(models.TextChoices):
    """ Пол пациента """
    FEMALE = 'женщина'
    MALE = 'мужчина'


class Patient(models.Model):
    """ Модель сущности пациента """
    birthday = models.DateField(verbose_name='День рождения', **NULLABLE)
    address = models.CharField(max_length=255, verbose_name='Адресс проживания', **NULLABLE)
    blood_type = models.CharField(
        max_length=10,
        choices=BloodType.choices,
        verbose_name='Группа крови',
        **NULLABLE
    )
    gender = models.CharField(
        max_length=7,
        choices=GenderChoice.choices,
        verbose_name='Пол пациента',
        **NULLABLE
    )
    place_of_work = models.CharField(max_length=255, verbose_name='Место работы', **NULLABLE)
    hobbies = models.CharField(max_length=255, verbose_name='Увлечения', **NULLABLE)
    discount_status = models.SmallIntegerField(verbose_name='Скидка пациента на услуги', default=0)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name='Владелец'
    )

    def __str__(self):
        return f'{self.owner}'

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class Time(models.Model):
    """ Время приема """
    time = models.TimeField(verbose_name='Время для записи на прием')

    def __str__(self):
        return f'{self.time}'

    class Meta:
        verbose_name = 'Время приема'
        verbose_name_plural = 'Время приема'


class StatusAppointment(models.TextChoices):
    """ Статус записи на прием """
    ACTIVE = 'Активный'
    CANCEL = 'Отменён'
    COMPLETED = 'Завершен'


class Appointment(models.Model):
    """ Запись пациента на прием """
    date = models.DateField(**NULLABLE, verbose_name='Дата приема')
    time = models.ForeignKey(
        Time,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name='Время приема')
    doctor = models.ForeignKey(
        Doctor,
        related_name='doctor_name',
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name='Врач'
    )
    status = models.CharField(
        max_length=8,
        choices=StatusAppointment.choices,
        verbose_name='Статус записи на прием',
        default=StatusAppointment.ACTIVE
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name='Владелец'
    )

    def __str__(self):
        return f'{self.doctor}'

    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'


class Feedback(models.Model):
    """ Модель - Отзыв о клинике """
    text = models.TextField(max_length=1500, verbose_name='Отзыв о центре медицинской диагностики')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Отображать отзыв о клинике')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name='Владелец',
        **NULLABLE
    )

    def __str__(self):
        return f'{self.owner}'

    class Meta:
        verbose_name = 'Отзыв клиента (пациента)'
        verbose_name_plural = 'Отзывы клиентов (пациентов)'
