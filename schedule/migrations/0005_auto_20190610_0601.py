# Generated by Django 2.2.2 on 2019-06-10 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20190113_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='term',
            field=models.CharField(db_index=True, default='2018-2019-03', max_length=64),
        ),
    ]