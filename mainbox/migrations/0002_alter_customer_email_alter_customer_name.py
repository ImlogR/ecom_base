# Generated by Django 4.2 on 2023-04-27 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainbox', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
