# Generated by Django 3.1 on 2020-08-21 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoteApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotes',
            name='author',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
    ]