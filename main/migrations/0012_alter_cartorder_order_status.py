# Generated by Django 4.2.4 on 2023-09-28 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_cartorder_order_status_alter_cartorderitems_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_status',
            field=models.CharField(choices=[('process', 'In Process'), ('deliverd', 'Deliverd')], default='process', max_length=100),
        ),
    ]