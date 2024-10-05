# Generated by Django 5.1.1 on 2024-10-05 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0011_devoluciones_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('contenido', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
