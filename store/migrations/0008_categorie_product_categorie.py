# Generated by Django 4.2.2 on 2023-07-19 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='categorie',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='store.categorie'),
        ),
    ]
