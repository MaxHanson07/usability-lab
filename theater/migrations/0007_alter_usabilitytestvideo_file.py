# Generated by Django 4.1.7 on 2023-03-22 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0006_alter_testnotes_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usabilitytestvideo',
            name='file',
            field=models.FileField(null=True, upload_to='', verbose_name=''),
        ),
    ]
