# Generated by Django 4.2.4 on 2023-10-11 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_remove_customuser_mobile_number1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
