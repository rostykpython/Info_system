# Generated by Django 4.1.2 on 2022-10-17 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transport_app", "0012_summarytaxes_summary_vat_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="summarytaxes",
            name="summary_vat",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
