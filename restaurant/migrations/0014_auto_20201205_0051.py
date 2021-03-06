# Generated by Django 2.2.5 on 2020-12-05 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0013_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='calories',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='product',
            name='fats',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/product'),
        ),
    ]
