# Generated by Django 5.1.1 on 2024-10-04 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0009_devoluciones_estado_devoluciones_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devoluciones',
            name='usuario',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
