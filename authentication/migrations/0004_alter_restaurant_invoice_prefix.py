# Generated by Django 4.1.3 on 2023-03-25 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_restaurant_invoice_prefix"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurant",
            name="invoice_prefix",
            field=models.CharField(default="INV-", max_length=16),
        ),
    ]