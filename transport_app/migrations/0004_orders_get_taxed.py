# Generated by Django 4.1.2 on 2022-10-16 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transport_app", "0003_workers_worker_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="orders",
            name="get_taxed",
            field=models.BooleanField(default=False),
        ),
    ]