# Generated by Django 3.1.7 on 2021-04-02 15:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vipcontacts', '0007_delete_relationship'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('dt_obsolete', models.DateTimeField(null=True)),
                ('type', models.IntegerField(choices=[(0, 'Wife'), (1, 'Husband'), (2, 'Son'), (3, 'Daughter'), (4, 'Father'), (5, 'Mother'), (6, 'Grandfather'), (7, 'Grandmother'), (8, 'Grandson'), (9, 'Granddaughter')])),
                ('destiny', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='destiny', to='vipcontacts.person')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin', to='vipcontacts.person')),
            ],
            options={
                'db_table': 'relationship',
                'managed': True,
            },
        ),
    ]
