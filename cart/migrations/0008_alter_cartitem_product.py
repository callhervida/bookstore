# Generated by Django 4.2.4 on 2023-10-21 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_book_average_rate_book_count_comment_comment'),
        ('cart', '0007_alter_cart_owner_userorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='book.book'),
        ),
    ]
