# Generated by Django 4.2.1 on 2023-07-02 21:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("triangle", "0007_logtriangle_response_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="logtriangle",
            name="bad_method",
        ),
    ]
