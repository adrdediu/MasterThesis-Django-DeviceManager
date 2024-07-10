# Generated by Django 5.0.1 on 2024-07-10 10:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_alter_device_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorizationlist',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('PAUSED', 'Paused'), ('COMPLETED', 'Completed'), ('CANCELED', 'Canceled'), ('UNKNOWN', 'Unknown')], default='ACTIVE', max_length=10),
        ),
        migrations.CreateModel(
            name='ExtendedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('rank', models.CharField(blank=True, choices=[('PROF', 'Profesor (Professor)'), ('CONF', 'Conferentiar (Associate Professor)'), ('LECTOR', 'Șef lucrări (Lecturer)'), ('ASIST', 'Asistent universitar (Assistant)'), ('ENG', 'Engineer')], max_length=20)),
                ('admin_rank', models.CharField(blank=True, choices=[('RECTOR', 'Rector'), ('PRORECTOR', 'Vice-rector'), ('DECAN', 'Decan (Dean)'), ('PRODECAN', 'Prodecan (Vice-dean)'), ('DIR_DEPT', 'Director de departament (Head of department)'), ('SEF_DISC', 'Șef de disciplină (Head of a subject)')], max_length=20)),
                ('building', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='devices.building')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='extended_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]