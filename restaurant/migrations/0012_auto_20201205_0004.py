# Generated by Django 2.2.5 on 2020-12-05 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0011_restaurant_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('desc', models.TextField(blank=True, max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='companies',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='companies',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='companies',
            name='phone',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('desc', models.TextField(blank=True, max_length=200)),
                ('calories', models.DecimalField(decimal_places=10, max_digits=19)),
                ('fats', models.DecimalField(decimal_places=10, max_digits=19)),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.Category')),
            ],
        ),
    ]