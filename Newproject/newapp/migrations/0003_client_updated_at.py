# Generated by Django 4.1.4 on 2023-02-27 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0002_client_alter_employee_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
