# Generated by Django 5.0.2 on 2024-04-17 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_alter_docmember_useremail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roommember',
            name='room',
        ),
        migrations.DeleteModel(
            name='DocMember',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.DeleteModel(
            name='RoomMember',
        ),
    ]
