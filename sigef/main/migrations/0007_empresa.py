# Generated by Django 2.1.5 on 2019-01-12 17:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20190109_0559'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('razon_social', models.CharField(max_length=250, unique=True)),
                ('rfc', models.CharField(default='RFC', max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message='El R.F.C. debe tener 13 caracteres.', regex='^.{13}$')])),
            ],
            options={
                'verbose_name_plural': 'Empresa',
            },
        ),
    ]
