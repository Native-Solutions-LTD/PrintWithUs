# Generated by Django 4.0.1 on 2022-03-14 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pwuDB', '0007_orders_cancellation_reason'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='image',
        ),
    ]
