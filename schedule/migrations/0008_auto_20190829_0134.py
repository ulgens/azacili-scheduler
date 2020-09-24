from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_auto_20190829_0057'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='program',
            options={'ordering': ['code']},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['code']},
        ),
    ]
