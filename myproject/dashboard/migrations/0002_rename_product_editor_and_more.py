# Generated by Django 5.0.2 on 2024-02-22 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product',
            new_name='Editor',
        ),
        migrations.RenameField(
            model_name='editor',
            old_name='description',
            new_name='content',
        ),
    ]
