# Generated by Django 3.1 on 2020-10-02 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201002_1739'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='image',
            new_name='Profilepic',
        ),
    ]