# Generated by Django 5.2.1 on 2025-06-02 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dds', '0002_alter_status_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название'),
        ),
    ]
