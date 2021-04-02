# Generated by Django 2.2 on 2021-04-02 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='article/%Y%m%d/'),
        ),
        migrations.AddField(
            model_name='articlepost',
            name='brief',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]