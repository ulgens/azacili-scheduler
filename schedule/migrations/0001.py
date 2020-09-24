import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('code', models.CharField(max_length=8)),
            ],
            options={
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=64)),
                ('term', models.CharField(db_index=True, default='2019-2020-01', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Bölüm Adı')),
                ('code', models.CharField(max_length=8, verbose_name='Bölüm Kodu')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('code', models.IntegerField(verbose_name='CRN')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='schedule.course')),
                ('lecturer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='schedule.instructor')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='schedule.program'),
        ),
        migrations.AlterField(
            model_name='course',
            name='term',
            field=models.CharField(db_index=True, default='2020-2021-01', max_length=64),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveSmallIntegerField(null=True)),
                ('room', models.CharField(max_length=16, null=True)),
                ('day', models.PositiveSmallIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], null=True)),
                ('start_time', models.TimeField(null=True, verbose_name='Ders başlangıç saati')),
                ('end_time', models.TimeField(null=True, verbose_name='Ders bitiş saati')),
                ('building', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lessons', to='schedule.building')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lessons', to='schedule.section')),
            ],
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
