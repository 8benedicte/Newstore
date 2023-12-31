# Generated by Django 4.2.2 on 2023-08-12 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='orders',
            field=models.ManyToManyField(related_name='carts', to='store.order'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.category'),
        ),
    ]
