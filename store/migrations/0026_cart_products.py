# Generated by Django 4.2.3 on 2024-02-02 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_remove_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
    ]
