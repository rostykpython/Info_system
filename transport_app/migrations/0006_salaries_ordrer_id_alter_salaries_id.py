# Generated by Django 4.1.2 on 2022-10-16 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("transport_app", "0005_alter_companytaxes_create_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="salaries",
            name="ordrer_id",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                to="transport_app.orders",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="salaries",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
