# Generated by Django 4.2.1 on 2023-05-19 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0006_alter_table_linkipclick_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="table_personallink",
            name="sequence",
            field=models.IntegerField(default=0),
        ),
    ]