from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0008_auto_20190829_0134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='building',
            options={'ordering': ('code',)},
        ),
    ]
