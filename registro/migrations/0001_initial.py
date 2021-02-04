# Generated by Django 2.2.6 on 2019-10-22 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dato', models.CharField(max_length=100, verbose_name='Datos del R.N.')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora Nacimiento')),
                ('sexo', models.CharField(max_length=20)),
                ('dni', models.CharField(max_length=20, verbose_name='DNI - Madre o Titular')),
                ('reg', models.BooleanField(default=False)),
            ],
        ),
    ]
