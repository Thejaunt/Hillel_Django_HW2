# Generated by Django 4.2.1 on 2023-07-15 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("scrapping", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quote",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="scrapping.author"
            ),
        ),
    ]
