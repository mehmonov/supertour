# Generated by Django 5.1.5 on 2025-01-17 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='number_of_people',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='total_price',
        ),
        migrations.AddField(
            model_name='booking',
            name='first_name',
            field=models.CharField(default=99999, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='phone_number',
            field=models.CharField(default=9999, max_length=15, verbose_name='Telefon raqami'),
            preserve_default=False,
        ),
    ]
