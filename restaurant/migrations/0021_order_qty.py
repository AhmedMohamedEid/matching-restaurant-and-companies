# Generated by Django 2.2.5 on 2020-12-05 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0020_order_company_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='qty',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]