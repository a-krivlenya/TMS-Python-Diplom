# Generated by Django 5.0.7 on 2024-07-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0012_purchase_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchase",
            name="price",
            field=models.FloatField(),
        ),
    ]
