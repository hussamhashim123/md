# Generated by Django 4.2.4 on 2023-08-18 21:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="money",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
