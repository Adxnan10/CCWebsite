# Generated by Django 3.2.2 on 2021-06-12 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_alter_answer_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]