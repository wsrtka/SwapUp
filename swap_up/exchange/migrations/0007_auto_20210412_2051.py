# Generated by Django 2.2 on 2021-04-12 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0006_student_list_of_classes'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='group_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='class',
            name='room',
            field=models.CharField(default='zdalnie', max_length=20),
        ),
    ]
