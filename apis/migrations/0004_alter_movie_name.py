# Generated by Django 4.1.4 on 2022-12-28 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_remove_show_name_alter_booking_seat_alter_seat_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
