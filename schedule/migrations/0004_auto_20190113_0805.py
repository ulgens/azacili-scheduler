from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schedule', '0003_course_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='term',
            field=models.CharField(db_index=True, default='2018-2019-02', max_length=64),
        ),
    ]
