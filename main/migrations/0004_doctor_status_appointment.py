# Generated by Django 4.2.5 on 2023-09-13 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='status_appointment',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Статус врача, True - можно записаться на прем'),
        ),
    ]
