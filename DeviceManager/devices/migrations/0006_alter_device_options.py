# Generated by Django 5.0.1 on 2024-06-28 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_devicescan'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='device',
            options={'ordering': ['id']},
        ),
    ]