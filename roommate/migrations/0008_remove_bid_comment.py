# Generated by Django 3.1.7 on 2021-04-02 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roommate', '0007_auto_20210402_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='comment',
        ),
    ]
