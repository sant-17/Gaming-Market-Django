# Generated by Django 4.1.2 on 2022-11-17 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_alter_usuario_clave_alter_usuario_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compra_detalle',
            name='id_compra',
        ),
        migrations.RemoveField(
            model_name='compra_detalle',
            name='id_juego',
        ),
        migrations.AddField(
            model_name='juego',
            name='proveedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.proveedor'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Compra',
        ),
        migrations.DeleteModel(
            name='Compra_detalle',
        ),
    ]
