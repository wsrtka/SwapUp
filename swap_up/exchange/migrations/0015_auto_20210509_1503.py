# Generated by Django 3.1.2 on 2021-05-09 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0014_auto_20210509_1118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='subject_name',
            new_name='name',
        ),
    ]