# Generated by Django 2.1.5 on 2019-04-24 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_userquestion_point_obtenu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquestion',
            name='point_obtenu',
            field=models.FloatField(),
        ),
    ]
