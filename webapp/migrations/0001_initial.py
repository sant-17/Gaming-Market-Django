# Generated by Django 4.1 on 2022-09-11 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('fecha_nacimiento', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Juego',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('fecha_lanzamiento', models.DateField()),
                ('desarrollador', models.CharField(max_length=50)),
                ('editor', models.CharField(max_length=50, null=True)),
                ('descripcion', models.TextField()),
                ('esrb', models.CharField(choices=[('E', 'Everyone'), ('E10', 'Everyone 10+'), ('T', 'Teen'), ('M', 'Mature 17+'), ('AO', 'Adults Only 18+'), ('RP', 'Rating Pending')], default='RP', max_length=30)),
                ('stock', models.PositiveIntegerField()),
                ('precio', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('imagen', models.URLField(blank=True, null=True)),
                ('habilitado', models.BooleanField()),
                ('generos', models.ManyToManyField(to='webapp.genero')),
            ],
        ),
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('telefono', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('permisos', models.ManyToManyField(to='webapp.permiso')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Venta_detalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=15)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('id_juego', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.juego')),
                ('id_venta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.venta')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('clave', models.CharField(max_length=50)),
                ('id_permiso', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.rol')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('telefono', models.IntegerField()),
                ('fecha_nacimiento', models.DateField()),
                ('municipio_residencia', models.CharField(max_length=30)),
                ('direccion_residencia', models.TextField()),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Compra_detalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('id_compra', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.compra')),
                ('id_juego', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.juego')),
            ],
        ),
        migrations.AddField(
            model_name='compra',
            name='id_proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.proveedor'),
        ),
        migrations.AddField(
            model_name='compra',
            name='juegos',
            field=models.ManyToManyField(blank=True, through='webapp.Compra_detalle', to='webapp.juego'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='webapp.usuario'),
        ),
    ]
