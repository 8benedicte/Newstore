# Generated by Django 4.2.5 on 2023-10-10 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0004_alter_shopper_groups_alter_shopper_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopper',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='shopper_set', related_query_name='shopper', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='shopper',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='shopper_set', related_query_name='shopper', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
