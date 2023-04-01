# Generated by Django 4.1.3 on 2023-01-11 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("finance", "0001_initial"),
        ("authentication", "0002_restaurant_upi_id"),
        ("kitchen", "0002_staff"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="staff",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="kitchen.staff"
            ),
        ),
        migrations.AddField(
            model_name="customer",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="authentication.restaurant",
            ),
        ),
    ]
