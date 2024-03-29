# Generated by Django 4.0.4 on 2022-04-28 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vipcontacts', '0008_auto_20210427_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blob',
            name='mime',
            field=models.CharField(choices=[('image/png', 'image/png'), ('image/jpeg', 'image/jpeg'), ('text/plain', 'text/plain')], max_length=100),
        ),
        migrations.AlterField(
            model_name='log',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_person', to='vipcontacts.person'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='retypes',
            field=models.IntegerField(choices=[(0, 'Home'), (1, 'Work'), (3, 'Personal mobile'), (4, 'Work mobile'), (5, 'Others'), (6, 'Work fax'), (7, 'Work internal phone'), (8, 'Work internal mobile')]),
        ),
    ]
