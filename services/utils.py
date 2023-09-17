import calendar
from datetime import datetime
import random
import string
from pytils.translit import slugify
from uuid import uuid4

NULLABLE = {'blank': True, 'null': True}


def generation_password():
    """ Генератор пароля """
    characterList: str = ''
    characterList += string.ascii_letters
    new_password: list = []
    for i in range(20):
        # Выбирает случайный символ, из списка символов
        randomchar: chr = random.choice(characterList)
        # Добавляет выбранный символ
        new_password.append(randomchar)
    # Склеивает список символов в строку
    new_password: str = "".join(new_password)
    return new_password


def unique_slugify(instance, slug):
    """ Генератор уникальных SLUG для моделей, в случае существования такого SLUG. """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug


def parser_register_update_form(form_as_p):
    """ Читает сформированную строку forms.as_p, меняет под стиль сайта """
    form_list_modified: list = []
    form_list = form_as_p.split('\n')
    for line in form_list:
        # Текст - название формы
        if '<label' in line and 'Очистить' not in line and 'Удалить:' not in line:
            line_modified = f'<div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label' \
                            f'form-input-icon">' \
                            f'<div class="text-left">{line}</div>'
            form_list_modified.append(line_modified)

        # Ловит секцию <select><option></select>
        if '<select' in line or '<option' in line:
            form_list_modified.append(line)

        if '</select>' in line:
            line_modified = f'{line}' \
                            f'</div>'
            form_list_modified.append(line_modified)

        # Ловит ссылку на аватар
        if '<a href' in line:
            # Находит начало ссылки
            start = line.find('"')
            # Находит конец ссылки
            end = line.rfind('"')
            # Срезает строку, выделяя чистый путь к файлу
            line_modified = line[start+1:end]
            # Сборка html кода
            line_modified = f'<image src="{line_modified}" width="300" alt="Аватар"><br></div>'
            form_list_modified.append(line_modified)

        # Лечит баг
        if 'Изменить:' in line:
            line_modified = f'<div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label' \
                            f'form-input-icon">' \
                            f'<div class="text-left"><label for="avatar-clear_id">Изменить аватар</label></div>'
            form_list_modified.append(line_modified)

        # Сама форма, кроме отключенных и checkbox на очистку аватара
        if '<input' in line and 'disabled' not in line and 'checkbox' not in line:
            # Делает поле только для чтения
            if 'discount_status' in line:
                line = line.replace('>', 'readonly="readonly">')
            line_modified = f'{line}' \
                            f'</div>'
            form_list_modified.append(line_modified)

        # Ловит ссылки на сохранение формы Patient
        if 'type="hidden"' in line and 'disabled' not in line:
            line_modified = f'<div>{line}'
            form_list_modified.append(line_modified)

    return ''.join(form_list_modified)


def calendar_line_to_list():
    """
        Возвращает календарь на текущий месяц.
        В списке дни текущего месяца, прошлого и следующего месяца если неделя захватывает дни.
        Текущий год.
        Месяц в строке.
    """
    # Создает объект
    calendar_object = calendar.Calendar()
    days_list: list = []
    month_dict = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь'
    }

    # Получает текущую дату
    date_now = datetime.now()
    year_now = date_now.year
    month_now = date_now.month
    day_now = date_now.day

    # Создает список дней
    count: int = 0
    for date in calendar_object.itermonthdates(year_now, month_now):
        if count == 7:
            days_list.append(0)
            count = 0

        if month_now != date.month:
            days_list.append(' ')
        else:
            days_list.append(date.day)

        count += 1

    return days_list, year_now, month_dict[month_now], day_now, month_now
