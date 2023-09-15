# Generated by Django 4.2.5 on 2023-09-14 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='заголовок')),
                ('slug', models.CharField(max_length=255, verbose_name='url')),
                ('content', models.TextField(max_length=1500, verbose_name='содержимое')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='изображение')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('publication', models.BooleanField(default=False, verbose_name='признак публикации')),
                ('number_of_views', models.IntegerField(default=0, verbose_name='количество просмотров')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блоги',
            },
        ),
    ]
