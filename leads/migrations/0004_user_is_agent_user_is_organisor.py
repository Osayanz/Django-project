# Generated by Django 5.2.1 on 2025-06-18 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_rename_organization_agent_organisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_agent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organisor',
            field=models.BooleanField(default=True),
        ),
    ]
