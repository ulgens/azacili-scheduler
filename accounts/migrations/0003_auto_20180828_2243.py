from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schedule', '0001_initial'),
        ('accounts', '0002_user_lessons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='lessons',
        ),
        migrations.AddField(
            model_name='user',
            name='sections',
            field=models.ManyToManyField(to='schedule.Section'),
        ),
    ]
