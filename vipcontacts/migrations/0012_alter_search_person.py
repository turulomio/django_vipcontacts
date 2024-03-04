# Generated by Django 5.0.2 on 2024-03-04 19:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vipcontacts", "0011_alter_address_country_alter_log_retypes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="search",
            name="person",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="search",
                to="vipcontacts.person",
            ),
        ),
    ]