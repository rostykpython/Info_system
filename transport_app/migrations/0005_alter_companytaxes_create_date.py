# Generated by Django 4.1.2 on 2022-10-16 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transport_app", "0004_orders_get_taxed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="companytaxes",
            name="create_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
