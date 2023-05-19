# Generated by Django 4.2.1 on 2023-05-19 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0003_alter_table_businesscard_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="table_businesscard",
            name="color",
            field=models.CharField(default="#0068bd33", max_length=20),
        ),
        migrations.CreateModel(
            name="Table_linkIPClick",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("ip", models.CharField(max_length=100)),
                ("clickTime", models.DateTimeField(auto_now_add=True)),
                (
                    "link",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app1.table_personallink",
                    ),
                ),
            ],
        ),
    ]