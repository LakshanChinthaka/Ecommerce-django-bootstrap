# Generated by Django 4.2.4 on 2023-10-02 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_cartorder_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartorder',
            name='payment_method_choices',
        ),
        migrations.AddField(
            model_name='cartorder',
            name='payment_method',
            field=models.CharField(choices=[('online', 'Online'), ('cod', 'Cash on Delivery')], default='process', max_length=100),
        ),
    ]
