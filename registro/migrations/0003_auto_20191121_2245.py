# Generated by Django 2.2.4 on 2019-11-22 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0002_auto_20191106_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='neonato',
            name='transf',
            field=models.CharField(blank=True, choices=[('Ucin', 'Ucin'), ('InterMedio - 1', 'InterMedio - 1'), ('InterMedio - 2', 'InterMedio - 2')], max_length=20),
        ),
        migrations.AlterField(
            model_name='neonato',
            name='dato',
            field=models.CharField(help_text='Apellido Paterno  Apellido Materno  RN', max_length=100, verbose_name='Datos del R.N.'),
        ),
        migrations.AlterField(
            model_name='neonato',
            name='reg',
            field=models.BooleanField(default=False, help_text='Registrado-Marcara solo en Modulo cuando Neonato es Hospitalizado', verbose_name='Registrado'),
        ),
    ]