# Generated by Django 4.1.3 on 2023-01-11 19:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("authentication", "0002_restaurant_upi_id"),
        ("kitchen", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("contact", models.CharField(max_length=16, unique=True)),
                ("name", models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("subtotal", models.FloatField(default=0.0)),
                ("discount", models.FloatField(default=0.0)),
                ("cgst", models.FloatField(default=0.0)),
                ("sgst", models.FloatField(default=0.0)),
                ("total", models.FloatField(default=0.0)),
                (
                    "payment_type",
                    models.CharField(
                        choices=[("Cash", "Cash"), ("UPI", "Upi"), ("Card", "Card")],
                        default="Cash",
                        max_length=32,
                    ),
                ),
                ("finalized", models.BooleanField(default=False)),
                ("table", models.CharField(max_length=32)),
                ("invoice_number", models.PositiveBigIntegerField(default=1)),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="finance.customer",
                    ),
                ),
                (
                    "platform",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="kitchen.platform",
                    ),
                ),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="authentication.restaurant",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("quantity", models.IntegerField(default=0)),
                (
                    "size",
                    models.CharField(
                        choices=[("half", "Half"), ("full", "Full")],
                        default="full",
                        max_length=16,
                    ),
                ),
                ("cost", models.FloatField(default=0.0)),
                (
                    "dish",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="kitchen.dish",
                    ),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="finance.invoice",
                    ),
                ),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="authentication.restaurant",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="KOT",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                ("items", models.JSONField(default=[])),
                (
                    "bill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="finance.invoice",
                    ),
                ),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="authentication.restaurant",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
