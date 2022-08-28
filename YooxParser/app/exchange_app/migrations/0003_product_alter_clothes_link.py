# Generated by Django 4.0.5 on 2022-08-23 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0002_alter_clothes_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('group', models.CharField(max_length=100)),
                ('old_price', models.CharField(max_length=100, null=True)),
                ('discount', models.CharField(max_length=100, null=True)),
                ('new_price', models.CharField(max_length=100, null=True)),
                ('fullprice', models.CharField(max_length=100, null=True)),
                ('sizes', models.CharField(max_length=100, null=True)),
                ('colors', models.CharField(max_length=100, null=True)),
                ('link', models.CharField(max_length=200)),
                ('art', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='clothes',
            name='link',
            field=models.CharField(max_length=200),
        ),
    ]