# Generated by Django 4.0 on 2021-12-13 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20211201_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/gallery')),
                ('thumb', models.ImageField(blank=True, null=True, upload_to='products/gallery/thumbs')),
            ],
        ),
    ]