# Generated by Django 5.2 on 2025-04-30 07:24

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_order_orderitem'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Баасы (сом)'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(blank=True, max_length=100, verbose_name='Автордун аты')),
                ('text', models.TextField(verbose_name='Пикирдин тексти')),
                ('rating', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Рейтинг')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Түзүлгөн убакыт')),
                ('is_approved', models.BooleanField(default=False, help_text='Сайтта көрсөтүү үчүн белгилеңиз', verbose_name='Жактырылды')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Башкы бетте көрсөтүлөт')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='menu.product', verbose_name='Товар')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Колдонуучу')),
            ],
            options={
                'verbose_name': 'Пикир',
                'verbose_name_plural': 'Пикирлер',
                'ordering': ('-created_at',),
            },
        ),
    ]
