# Generated by Django 3.1.2 on 2021-05-09 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0015_auto_20210509_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='other_student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wantee', to='exchange.student'),
        ),
    ]
