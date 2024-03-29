# Generated by Django 4.1.3 on 2023-02-11 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0005_alter_invoice_staff"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="kot",
            name="items",
        ),
        migrations.AddField(
            model_name="order",
            name="kot",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="finance.kot"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="quantity",
            field=models.IntegerField(default=1),
        ),
    ]
