# Generated by Django 2.2.5 on 2020-12-04 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_auto_20201204_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='desc',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
