# Generated by Django 4.0 on 2022-02-21 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_auto_20211123_2207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]