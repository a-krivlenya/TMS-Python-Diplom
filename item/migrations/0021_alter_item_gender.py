# Generated by Django 5.1.7 on 2025-03-09 21:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0020_alter_comment_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="gender",
            field=models.CharField(choices=[("M", "Man"), ("W", "Woman")], max_length=10),
        ),
    ]
