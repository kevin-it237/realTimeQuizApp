# Generated by Django 2.1.5 on 2019-04-24 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquestion',
            name='point_obtenu',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
