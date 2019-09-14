# Generated by Django 2.1.5 on 2019-01-08 06:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_categoriatipoproveedor_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriatipoproveedor',
            name='categoria',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='categoriatipoproveedor',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', related_query_name='categoria', to='main.TipoProveedor'),
        ),
        migrations.AlterField(
            model_name='estadofactura',
            name='estado',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='tipocredito',
            name='plazo',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(7, 'El plazo debe ser mayor a 7 días.'), django.core.validators.MaxValueValidator(30, 'El plazo máximo es de 30 días.')]),
        ),
        migrations.AlterField(
            model_name='tipomoneda',
            name='moneda',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='tipomoneda',
            name='nomenclatura',
            field=models.CharField(max_length=3, unique=True),
        ),
        migrations.AlterField(
            model_name='tipoproveedor',
            name='tipo',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
