# Generated by Django 2.2.10 on 2020-02-28 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20200228_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='category',
            field=models.ManyToManyField(blank=True, to='tasks.Category'),
        ),
    ]