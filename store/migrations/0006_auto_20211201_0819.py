# Generated by Django 3.2.9 on 2021-12-01 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(blank=True, null=True),
        ),
    ]