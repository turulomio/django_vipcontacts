# Generated by Django 3.1.7 on 2021-04-08 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vipcontacts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='retypes',
            field=models.IntegerField(choices=[(0, 'Contact data changed'), (1, 'Contact data added'), (2, 'Contact data deleted'), (100, 'Personal')]),
        ),
        migrations.AlterField(
            model_name='phone',
            name='phone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='phone',
            name='retypes',
            field=models.IntegerField(choices=[(0, 'Home'), (1, 'Work'), (3, 'Personal mobile'), (4, 'Work mobile'), (5, 'Others'), (6, 'Work fax')]),
        ),
    ]