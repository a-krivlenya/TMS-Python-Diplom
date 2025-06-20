# Generated by Django 5.0.7 on 2024-07-17 12:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
        ("item", "0002_remove_item_created_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="myuser",
            name="items",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to="item.item",
            ),
        ),
    ]
