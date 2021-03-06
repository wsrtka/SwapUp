# Generated by Django 3.1.2 on 2021-05-09 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0013_auto_20210509_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='modification_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(max_length=60, null=True),
        ),
    ]
