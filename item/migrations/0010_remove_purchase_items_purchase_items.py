# Generated by Django 5.0.7 on 2024-07-19 13:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0009_alter_purchase_items"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="purchase",
            name="items",
        ),
        migrations.AddField(
            model_name="purchase",
            name="items",
            field=models.ManyToManyField(to="item.item"),
        ),
    ]
