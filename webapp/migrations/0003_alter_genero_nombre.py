# Generated by Django 4.1 on 2022-09-12 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_juego_multijugador_alter_juego_habilitado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genero',
            name='nombre',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]