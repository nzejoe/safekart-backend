# Generated by Django 3.2.9 on 2021-11-23 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_cartitem_item_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='carts.itemvariation'),
        ),
    ]
