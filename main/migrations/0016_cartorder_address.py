# Generated by Django 4.2.4 on 2023-10-02 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_cartorder_payment_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
