# Generated by Django 4.2.1 on 2023-05-20 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0007_table_personallink_sequence"),
    ]

    operations = [
        migrations.AddField(
            model_name="table_businesscard",
            name="description",
            field=models.CharField(default="", max_length=500),
        ),
    ]