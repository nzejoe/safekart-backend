# Generated by Django 3.2.9 on 2021-11-23 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_alter_cartitem_cart_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(max_length=100, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='cart_id',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='carts.cart'),
            preserve_default=False,
        ),
    ]
