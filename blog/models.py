from django.db import models

from config import settings
from services.utils import unique_slugify, NULLABLE


class Blog(models.Model):
    """ Модель статьи (блога) """
    name = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=255, verbose_name='url')
    content = models.TextField(max_length=1500, verbose_name='содержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    publication = models.BooleanField(default=False, verbose_name='признак публикации')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name='Владелец',
        **NULLABLE
    )
    number_of_views = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.name}'

    def delete(self, using=None, keep_parents=False):
        """ Удаление статьи """
        self.publication = False
        self.save()

    def save(self, *args, **kwargs):
        """ Сохранение полей модели при их отсутствии заполнения """
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
