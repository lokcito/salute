# Generated by Django 2.2.4 on 2021-02-14 05:23

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0020_auto_20210213_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='censo',
            name='ncama',
            field=models.CharField(max_length=250),
        ),
    ]
