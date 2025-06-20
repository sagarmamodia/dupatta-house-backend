# Generated by Django 5.2.1 on 2025-06-04 11:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_management', '0002_alter_products_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimages',
            old_name='url',
            new_name='file_id',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='amount_paid',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orders',
            name='contact_number',
            field=models.CharField(default=None, max_length=13),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productdiscountentries',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('discontinued', 'Discontinued')], default='active'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('shipped', 'Shipped'), ('cancelled', 'Cancelled')], default='pending'),
        ),
        migrations.AlterField(
            model_name='products',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price_per_unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders_management.orders')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders_management.products')),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_order_id', models.CharField(max_length=100, unique=True)),
                ('amount', models.PositiveIntegerField(help_text='Amount in paise (e.g. ₹1 = 100 paise), because Razorpay expects paise')),
                ('currency', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('failed', 'Failed')], default='created', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='orders_management.orders')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
