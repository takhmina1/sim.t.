# Generated by Django 5.1.4 on 2024-12-19 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Robot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(help_text="Двухсимвольная модель робота, например 'R2'", max_length=2, verbose_name='Модель')),
                ('version', models.CharField(help_text="Версия модели, например 'D2'", max_length=10, verbose_name='Версия')),
                ('created_at', models.DateTimeField(help_text='Дата и время производства робота', verbose_name='Дата производства')),
            ],
            options={
                'verbose_name': 'Робот',
                'verbose_name_plural': 'Роботы',
                'ordering': ['-created_at'],
            },
        ),
    ]
