from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('schedule', '0006_auto_20190805_0332'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='program',
            options={'ordering': ['name']},
        ),
    ]
