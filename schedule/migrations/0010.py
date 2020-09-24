from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('schedule', '0009_auto_20190901_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='schedule.program'),
        ),
        migrations.AlterField(
            model_name='course',
            name='term',
            field=models.CharField(db_index=True, default='2020-2021-01', max_length=64),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='building',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lessons', to='schedule.building'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lessons', to='schedule.section'),
        ),
        migrations.AlterField(
            model_name='section',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sections', to='schedule.course'),
        ),
        migrations.AlterField(
            model_name='section',
            name='lecturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sections', to='schedule.instructor'),
        ),
    ]
