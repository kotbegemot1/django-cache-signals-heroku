# Generated by Django 2.2.10 on 2020-02-26 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20200226_0652'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='todo_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
