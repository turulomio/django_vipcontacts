# Generated by Django 3.1.7 on 2021-04-02 16:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vipcontacts', '0010_auto_20210402_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('dt_obsolete', models.DateTimeField(null=True)),
                ('retypes', models.IntegerField(choices=[(0, 'Home'), (1, 'Work'), (2, 'Other')])),
                ('mail', models.CharField(max_length=100, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mail', to='vipcontacts.person')),
            ],
            options={
                'db_table': 'mails',
                'managed': True,
            },
        ),
    ]
