from django import template
from django.utils.safestring import mark_safe

from services.utils import parser_register_update_form

register = template.Library()


# Шаблонный фильтр
@register.filter
def mediapath(format_path):
    """ Фильтр. Возвращает модифицированную строку """
    return mark_safe(f'http://127.0.0.1:8000/media/{format_path}')


@register.filter
def login_form(form_as_p):
    """
        Фильтр. Авторизация пользователя.
        Получает form_as_p для возможной модификации.
        По факту создается новый html код с нужным представлением форм.
    """
    form_string: str = """
                <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label form-input-icon">
                    <i class="fa fa-envelope-o"></i>
                    <input type="text" name="username" class="mdl-textfield__input" placeholder="Email"
                    id="login-email" autocapitalize="none" autocomplete="username" maxlength="254" required>
                </div>
                <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label form-input-icon">
                    <i class="fa fa-key"></i>
                    <input type="password" name="password" class="mdl-textfield__input" placeholder="Password"
                    id="login-password" required>
                </div>
    """
    return mark_safe(form_string)


@register.filter
def registration_form(form_as_p):
    """
        Фильтр. Регистрация пользователя.
        Получает form_as_p для возможной модификации.
        По факту создается новый html код с нужным представлением форм.
    """
    form_string: str = """
                <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label form-input-icon">
                    <i class="fa fa-envelope-o"></i>
                    <input type="email" name="email" maxlength="254" autofocus class="mdl-textfield__input"
                    placeholder="Почта" required id="id_email">
                </div>
                <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label form-input-icon">
                    <i class="fa fa-key"></i>
                    <input type="password" name="password1" autocomplete="new-password" class="mdl-textfield__input"
                    placeholder="Пароль" required id="id_password1">
                </div>
                <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label form-input-icon">
                    <i class="fa fa-key"></i>
                    <input type="password" name="password2" autocomplete="new-password" class="mdl-textfield__input"
                    placeholder="Повторите пароль" required id="id_password2">
                </div>
                <span style="text-align: left">
                    <ul>
                        <li>Пароль не должен быть слишком похож на другую вашу личную информацию.</li>
                        <li>Ваш пароль должен содержать как минимум 8 символов.</li>
                        <li>Пароль не должен быть слишком простым и распространенным.</li>
                        <li>Пароль не может состоять только из цифр.</li>
                    </ul>
                </span>

    """
    return mark_safe(form_string)


@register.filter
def update_form(form_as_p):
    """
        Фильтр. Обновление пользователя.
        Получает form_as_p для возможной модификации.
        По факту создается новый html код с нужным представлением форм.
    """
    form_string: str = parser_register_update_form(form_as_p)
    return mark_safe(form_string)


@register.filter
def appointment_form(field):
    """
        Фильтр. Запись на прием.
        Получает form_as_p для возможной модификации.
        По факту создается новый html код с нужным представлением форм.
    """
    field = str(field)
    if 'name="date"' in field:
        field = field.replace('>', """ onfocus="(this.type='date')" onblur="(this.type='text')">""")

    return mark_safe(field)


@register.filter
def feedback_form(field):
    """
        Фильтр. Запись на прием.
        Получает form_as_p для возможной модификации.
        По факту создается новый html код с нужным представлением форм.
    """
    field = str(field)
    field = field.replace('class="mdl-textfield__input"', 'class="form-control"')
    print(field)

    return mark_safe(field)


@register.filter
def reset_password_form(form_as_p):
    """
        Фильтр. Смена пароля.
        Получает form_as_p для возможной модификации.
        По факту создается новый html код с нужным представлением форм.
    """
    form_string: str = """
                <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label form-input-icon">
                    <i class="fa fa-envelope-o"></i>
                    <input type="email" name="email" class="mdl-textfield__input" autocomplete="email" maxlength="254"
                    required id="id_email">
                </div>
    """
    return mark_safe(form_string)


@register.filter
def date_modified(date):
    """ Выделяет из даты день. """
    return date.day


@register.filter
def time_modified(time):
    """ Убирает : """
    time = str(time)
    time = time.replace(':', '')
    return time


@register.filter
def time_seconds_modified(time):
    """ Убирает : """
    time = str(time)
    time = time[0:5]
    return time


@register.filter
def str_modified(str_):
    """ Убирает : """
    str_ = str(str_)
    str_ = str_.replace(':', '')
    str_ = str_.replace('.', '')
    str_ = str_.replace(' ', '')
    return str_
