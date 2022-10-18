# Generated by Django 4.1.2 on 2022-10-16 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("transport_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanyTaxes",
            fields=[
                (
                    "id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="transport_app.orders",
                        unique=True,
                    ),
                ),
                ("profit", models.FloatField()),
                ("tax_on_profit", models.FloatField()),
                ("vat", models.FloatField()),
                ("create_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Workers",
            fields=[
                (
                    "worker_id",
                    models.BigIntegerField(
                        primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("phone", models.CharField(max_length=200)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("salary_per_month", models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name="orders",
            name="is_completed",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="Salaries",
            fields=[
                (
                    "id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="transport_app.orders",
                        unique=True,
                    ),
                ),
                ("salary_per_order", models.FloatField()),
                ("tax_on_profit", models.FloatField()),
                ("military_tax", models.FloatField()),
                ("euv", models.FloatField()),
                (
                    "worker_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="transport_app.workers",
                    ),
                ),
            ],
        ),
    ]
