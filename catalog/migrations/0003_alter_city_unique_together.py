# Generated by Django 4.2.1 on 2023-06-16 18:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_alter_client_email"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="city",
            unique_together={("name", "state")},
        ),
    ]
