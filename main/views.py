import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, DeleteView, DetailView

from blog.models import Blog
from main.forms import AppointmentForm, FeedbackForm
from main.models import Doctor, Appointment, Time, Patient, Feedback
from services.utils import calendar_line_to_list
from users.models import User


# Create your views here.
class HomeView(ListView):
    """ Главная страница """
    model = User
    template_name = 'main/home.html'
    extra_context = {
        'title': ''
    }

    def get_context_data(self, **kwargs):
        """ Делает набор данных из раззных моделей """
        context_data = super().get_context_data(**kwargs)

        # Передает в doctors объекты докторов
        # Получает, всех докторов
        doctor_list = Doctor.objects.all()
        # Количество выводимых врачей
        count: int = 5
        count_doctor = Doctor.objects.all().count()
        if count_doctor < count:
            count = count_doctor
        # Список случайных объектов (Докторов)
        doctor_random_list: list = []
        # В случае существования докторов в БД
        if doctor_list:
            doctor_random_list = random.sample(list(doctor_list), count)
        context_data['doctors'] = doctor_random_list

        # Передает в feedbacks объекты отзывов
        # Получает, все отзывы
        feedback_list = Feedback.objects.filter(is_active=True)
        # Количество выводимых отзывов
        count: int = 5
        count_feedback = Feedback.objects.filter(is_active=True).count()
        if count_feedback < count:
            count = count_feedback
        # Список случайных объектов (Отзывы)
        feedback_random_list: list = []
        # В случае существования отзывов в БД
        if feedback_list:
            feedback_random_list = random.sample(list(feedback_list), count)
        context_data['feedbacks'] = feedback_random_list

        # Передает в feedbacks объекты отзывов
        # Получает, все отзывы
        blog_list = Blog.objects.filter(publication=True).order_by("-date_time")
        blog_list_: list = []
        if blog_list.count() >= 2:
            blog_list_.append(blog_list[0])
            blog_list_.append(blog_list[1])
        context_data['blog_list'] = blog_list_

        return context_data


class RightsContentView(TemplateView):
    """  """
    template_name = 'main/rights_content.html'


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    """ Создание записи на прием """
    model = Appointment
    form_class = AppointmentForm

    def get_success_url(self):
        """ Берем id из данного объекта """
        return reverse_lazy('main:appointments_user')

    def form_valid(self, form):
        """ Автоматически сохраняет текущего пользователя в поле user """
        # Создает форму в памяти, без отправки в бд
        self.object = form.save(commit=False)
        # Передает текущего пользователя в user
        self.object.owner = self.request.user
        # Сохраняет в бд
        self.object.save()

        return super(AppointmentCreateView, self).form_valid(form)


class AppointmentUserListView(LoginRequiredMixin, ListView):
    """ Список записей принадлежащих авторизованному пользователю """
    model = Appointment

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        """ Делает набор данных из раззных моделей """
        context_data = super().get_context_data(**kwargs)

        # Передача календаря
        days, year, month, day, month_int = calendar_line_to_list()
        context_data['days'] = days
        context_data['year'] = year
        context_data['month'] = month
        context_data['day_now'] = day

        return context_data


class AppointmentListView(LoginRequiredMixin, ListView):
    """ Список всех записей """
    model = Appointment
    template_name = 'main/appointment_list_all.html'

    def get_context_data(self, **kwargs):
        """ Делает набор данных из раззных моделей """
        context_data = super().get_context_data(**kwargs)

        # Передача календаря
        days, year, month, day, month_int = calendar_line_to_list()
        context_data['days'] = days
        context_data['year'] = year
        context_data['month'] = month
        context_data['day_now'] = day

        # Передает всех врачей
        doctors = Doctor.objects.all()
        context_data['doctors_list'] = doctors

        # Передает время
        times = Time.objects.all()
        context_data['times_list'] = times

        return context_data


class AppointmentDoctorListView(LoginRequiredMixin, ListView):
    """ Список записей для врача """
    model = Appointment
    template_name = 'main/appointment_list_doctor.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        doctor = Doctor.objects.filter(owner=self.request.user)
        queryset = queryset.filter(doctor=doctor[0])
        return queryset

    def get_context_data(self, **kwargs):
        """ Делает набор данных из раззных моделей """
        context_data = super().get_context_data(**kwargs)

        # Передача календаря
        days, year, month, day, month_int = calendar_line_to_list()
        context_data['days'] = days
        context_data['year'] = year
        context_data['month'] = month
        context_data['day_now'] = day

        # Передает время
        times = Time.objects.all()
        context_data['times_list'] = times

        return context_data


class UserProfileView(LoginRequiredMixin, DetailView):
    """ Просмотр профиля пациента, фитча для врача """
    model = User
    template_name = 'main/user_profile.html'

    def get_context_data(self, **kwargs):
        """ Делает набор данных из раззных моделей """
        context_data = super().get_context_data(**kwargs)

        # Передача календаря
        user = context_data['object']
        patient = Patient.objects.filter(owner=user)
        context_data['patient'] = patient[0]

        return context_data


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление записи """
    model = Appointment
    success_url = reverse_lazy('main:appointments_user')


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    """ Создание отзыва пользователя """
    model = Feedback
    form_class = FeedbackForm

    def get_success_url(self):
        """ Редирект на страницу """
        return reverse_lazy('main:user_list_feedback')

    def form_valid(self, form):
        """ Автоматически сохраняет текущего пользователя в поле user """
        # Создает форму в памяти, без отправки в бд
        self.object = form.save(commit=False)
        # Передает текущего пользователя в user
        self.object.owner = self.request.user
        # Сохраняет в бд
        self.object.save()

        return super(FeedbackCreateView, self).form_valid(form)


class FeedbackUserListView(LoginRequiredMixin, ListView):
    """ Просмотр отзывов данного пользователя """
    model = Feedback
    template_name = 'main/feedback_user_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Feedback.objects.filter(owner=self.request.user)
        return queryset


class FeedbackDeleteView(LoginRequiredMixin, DeleteView):
    """ Удаление записи """
    model = Feedback
    success_url = reverse_lazy('main:user_list_feedback')


class FeedbackListView(LoginRequiredMixin, ListView):
    """ Просмотр отзывов всех пользователей """
    model = Feedback
    template_name = 'main/feedback_list.html'
