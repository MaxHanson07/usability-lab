# Generated by Django 4.1.7 on 2023-03-20 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theater', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usabilitytest',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='usabilitytest',
            name='moderator',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usabilitytest',
            name='test_date',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='UsabilityTestVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usability_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='theater.usabilitytest')),
            ],
        ),
    ]