# Generated by Django 3.1.7 on 2021-03-21 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210321_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='featured',
        ),
    ]
