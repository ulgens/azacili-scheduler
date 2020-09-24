from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='name',
            field=models.CharField(max_length=1024),
        ),
    ]
