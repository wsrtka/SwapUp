# Generated by Django 3.2 on 2021-04-12 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0006_student_list_of_classes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]