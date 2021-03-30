# Generated by Django 2.2.4 on 2021-03-25 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0022_auto_20210325_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagare',
            name='check',
            field=models.BooleanField(default=False, help_text='Completa Informacion', verbose_name='Revisado'),
        ),
        migrations.AlterField(
            model_name='pagare',
            name='obs',
            field=models.CharField(default=False, max_length=200, verbose_name='Deposito/Garantia'),
        ),
        migrations.AlterField(
            model_name='pagare',
            name='ref',
            field=models.TextField(default=False, help_text='Observaciones de Acreditacion', max_length=100, verbose_name='Acredita-Obs'),
        ),
    ]
