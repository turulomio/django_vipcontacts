# Generated by Django 3.1.7 on 2021-04-02 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vipcontacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='destiny',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='destiny', to='vipcontacts.person'),
        ),
    ]