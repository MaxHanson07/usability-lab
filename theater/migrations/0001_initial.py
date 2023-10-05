# Generated by Django 4.1.7 on 2023-03-20 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsabilityTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('moderator', models.CharField(max_length=100)),
                ('test_date', models.DateTimeField()),
                ('description', models.TextField()),
            ],
        ),
    ]