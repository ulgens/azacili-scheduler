from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lessons',
            field=models.ManyToManyField(to='schedule.Lesson'),
        ),
    ]
