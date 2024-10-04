# Generated by Django 5.1.1 on 2024-10-02 18:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0008_tallas_producto_informacion_alter_producto_nombre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='devoluciones',
            name='estado',
            field=models.IntegerField(choices=[(1, 'Pendiente'), (2, 'Aceptada'), (3, 'Rechazada')], default=1),
        ),
        migrations.AddField(
            model_name='devoluciones',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
