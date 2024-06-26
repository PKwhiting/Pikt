# Generated by Django 3.2.23 on 2024-06-10 23:37

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(blank=True, max_length=17, null=True)),
                ('stock_number', models.CharField(blank=True, max_length=256, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('make', models.CharField(blank=True, max_length=256, null=True)),
                ('model', models.CharField(blank=True, max_length=256, null=True)),
                ('trim', models.CharField(blank=True, max_length=256, null=True)),
                ('primary_damage', models.CharField(blank=True, max_length=256, null=True)),
                ('secondary_damage', models.CharField(blank=True, max_length=256, null=True)),
                ('yard', models.CharField(blank=True, max_length=256, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('marker', models.CharField(blank=True, max_length=10000, null=True)),
                ('row', models.CharField(blank=True, max_length=256, null=True)),
                ('category', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('engine', models.CharField(blank=True, max_length=256, null=True)),
                ('mileage', models.CharField(blank=True, max_length=256, null=True)),
                ('transmission', models.CharField(blank=True, max_length=256, null=True)),
                ('body_type', models.CharField(blank=True, max_length=256, null=True)),
                ('drivetrain', models.CharField(blank=True, max_length=256, null=True)),
                ('exterior_primary_color', models.CharField(blank=True, max_length=256, null=True)),
                ('exterior_primary_paint_code', models.CharField(blank=True, max_length=256, null=True)),
                ('exterior_secondary_color', models.CharField(blank=True, max_length=256, null=True)),
                ('exterior_secondary_paint_code', models.CharField(blank=True, max_length=256, null=True)),
                ('interior_primary_color', models.CharField(blank=True, max_length=256, null=True)),
                ('interior_primary_paint_code', models.CharField(blank=True, max_length=256, null=True)),
                ('interior_secondary_color', models.CharField(blank=True, max_length=256, null=True)),
                ('interior_secondary_paint_code', models.CharField(blank=True, max_length=256, null=True)),
                ('total_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('for_sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('bid_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('auction_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('buyer_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('internet_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tow_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('dismantler_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('storage_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pullout_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('misc_fee', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('buyer', models.CharField(blank=True, max_length=256, null=True)),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('seller_type', models.CharField(blank=True, choices=[('COPART', 'COPART'), ('IAA', 'IAA'), ('Street', 'Street'), ('Charity', 'Charity'), ('Vendor', 'Vendor')], max_length=256, null=True)),
                ('seller_first_name', models.CharField(blank=True, max_length=256, null=True)),
                ('seller_last_name', models.CharField(blank=True, max_length=256, null=True)),
                ('seller_phone', models.CharField(blank=True, max_length=256, null=True)),
                ('seller_email', models.EmailField(blank=True, max_length=256, null=True)),
                ('seller_address', models.CharField(blank=True, max_length=256, null=True)),
                ('seller_city', models.CharField(blank=True, max_length=256, null=True)),
                ('seller_state', models.CharField(blank=True, max_length=256, null=True)),
                ('possession_date', models.DateField(blank=True, null=True)),
                ('cleared_date', models.DateField(blank=True, null=True)),
                ('towed_by', models.CharField(blank=True, max_length=256, null=True)),
                ('inventoried_date', models.DateField(blank=True, null=True)),
                ('dismantled_by', models.CharField(blank=True, max_length=256, null=True)),
                ('dismantled_date', models.DateField(blank=True, null=True)),
                ('crush_date', models.DateField(blank=True, null=True)),
                ('sold_date', models.DateField(blank=True, null=True)),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_5', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_6', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_7', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_8', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_9', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_10', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='company.company')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='company.location')),
            ],
        ),
        migrations.CreateModel(
            name='PartPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parts', models.TextField(blank=True, help_text='Comma-separated list of parts')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='part_preferences', to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_number', models.CharField(blank=True, max_length=50, null=True)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('grade', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1)),
                ('interchange', models.CharField(blank=True, max_length=5000, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('height', models.IntegerField(blank=True, null=True)),
                ('width', models.IntegerField(blank=True, null=True)),
                ('length', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Listed', 'Listed'), ('Sold', 'Sold'), ('Removed', 'Removed'), ('Pending', 'Pending'), ('On Hold', 'On Hold')], default='Pending', max_length=50)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_5', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_6', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_7', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_8', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_9', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('image_10', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboards.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=36)),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_address', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('shipping_label', models.FileField(blank=True, null=True, upload_to='shipping_labels/')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=50)),
                ('part_object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboards.part')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='inventory_files/')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('owner', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='core',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interchange', models.CharField(max_length=100)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cores', to='company.company')),
            ],
        ),
    ]
