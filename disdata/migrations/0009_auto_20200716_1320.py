# Generated by Django 3.0.7 on 2020-07-16 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disdata', '0008_pincode_is_alerted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='verified',
            field=models.BooleanField(default=True),
        ),
    ]
