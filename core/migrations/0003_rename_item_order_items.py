# Generated by Django 5.0.7 on 2024-07-19 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_orderitem_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='item',
            new_name='items',
        ),
    ]
