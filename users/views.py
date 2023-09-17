from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetDoneView, PasswordContextMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, CreateView, FormView, TemplateView
from pip._internal.utils._jaraco_text import _

from main.forms import PatientForm
from main.models import Patient
from services.utils import generation_password
from config import settings
from users.forms import UserRegisterForm, UserForm
from users.models import User
from django.forms import inlineformset_factory


class RegisterView(CreateView):
    """ Регистрация пользователя """
    model = User
    form_class = UserRegisterForm

    def form_valid(self, form):
        """ Дружественное письмо на почту пользователя, после регистрации """
        # Работа с пользователем
        new_user = form.save()
        uid = urlsafe_base64_encode(force_bytes(new_user.pk))
        new_token = token_generator.make_token(new_user)
        activation_url = reverse_lazy('users:verify_email', kwargs={'uidb64': uid, 'token': new_token})
        send_mail(
            subject='Центр медицинской диагностики - Активация учетной записи',
            message=f'Убедительная просьба:'
                    f' если хотите закончить регистрацию, пройдите по ссылке: http://127.0.0.1:8000/{ activation_url }',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
            fail_silently=False
        )
        return redirect('users:confirm_email')


class UserActivate(View):
    """ Активация пользователя из письма """
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        # Сравнение токенов
        if user is not None and token_generator.check_token(user, token):
            # Создает пациента данному пользователю (Запись в БД)
            Patient.objects.create(
                owner=user
            )

            # В случае удачи, активирует нового пользователя флагом True,
            # сохраняет обЪект, логинится и отправляет письмо на почту
            user.email_verify = True
            user.save()
            login(request, user)
            send_mail(
                subject='Центр медицинской диагностики - Успешная активация',
                message=f'Вы успешно активировали учетную запись!\nС уважением администрация сервиса.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            return redirect('users:user_activate')
        return redirect('users:invalid_user_activate')

    @staticmethod
    def get_user(uidb64):
        """ Получение пользователя """
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


class InvalidUserActivate(TemplateView):
    """ Случай неудачной активации """
    template_name = 'users/invalid_user_activate.html'


class UserPasswordResetView(PasswordContextMixin, FormView):
    """ Сброс пароля, генерация нового с отправкой на email """
    form_class = PasswordResetForm
    success_url = reverse_lazy("users:password_reset_done")
    title = _("Password reset")
    template_name = 'users/password_reset_form.html'

    def form_valid(self, form):
        """ Получает email, по email получает пользователя, генерирует и присваивает новый пароль,
        отправляет пароль на почту  """
        user_email: str = self.request.POST.get('email')
        new_password: str = generation_password()
        user_object: object = User.objects.get(email=user_email)
        send_mail(
            subject='Центр медицинской диагностики - Восстановление пароля',
            message=f'Вас приветствует администрация Центра медицинской диагностики.'
                    f'\nВы запросили новый пароль для {user_email}.\nВаш новый пароль: {new_password}'
                    f'\nС уважением администрация Центра медицинской диагностики.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email]
        )
        user_object.set_password(new_password)
        user_object.save()
        return super().form_valid(form)


class UserPasswordResetDoneView(PasswordResetDoneView):
    PasswordResetDoneView.template_name = 'users/password_reset_done.html'


class ProfileView(TemplateView):
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        """ Делает набор данных из раззных моделей """
        context_data = super().get_context_data(**kwargs)

        # Получает, пациента по пользователю
        patient = Patient.objects.filter(owner=self.request.user)
        if patient:
            patient = patient[0]
        # Передает пациента в context_data
        context_data['patient'] = patient

        return context_data


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование профиля """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    # def get_success_url(self, *args, **kwargs):
    #     return reverse('users:profile_update', args=[self.get_object().pk])

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        Patientformset = inlineformset_factory(User, Patient, form=PatientForm, extra=0)
        if self.request.method == 'POST':
            context_data['formset'] = Patientformset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = Patientformset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)
