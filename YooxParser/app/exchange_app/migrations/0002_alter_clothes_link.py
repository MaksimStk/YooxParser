# Generated by Django 4.0.5 on 2022-08-12 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothes',
            name='link',
            field=models.CharField(max_length=100),
        ),
    ]