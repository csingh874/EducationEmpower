# Generated by Django 3.2.5 on 2021-08-02 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_alter_coursesubheading_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesubheading',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
