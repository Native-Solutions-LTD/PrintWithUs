# Generated by Django 4.0.1 on 2022-03-14 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pwuDB', '0005_orders_cancellation_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='cancellation_reason',
        ),
    ]
