# Generated by Django 3.1.4 on 2021-01-06 13:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ilan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Başlık')),
                ('fiyat', models.IntegerField(verbose_name='Fiyat')),
                ('aciklama', models.TextField(verbose_name='Açıklama')),
                ('oda', models.IntegerField(verbose_name='Oda')),
                ('salon', models.IntegerField(verbose_name='Salon')),
                ('banyo', models.IntegerField(verbose_name='Banyo Sayısı')),
                ('il', models.TextField(verbose_name='İl')),
                ('ilçe', models.TextField(verbose_name='İlçe')),
                ('mahalle', models.TextField(verbose_name='Mahalle')),
                ('bina_kat', models.IntegerField(verbose_name='Binanın Kat Sayısı')),
                ('bina_yaş', models.IntegerField(verbose_name='Binanın Yaşı')),
                ('bulundugu_kat', models.TextField(verbose_name='Bulunduğu Kat')),
                ('m2', models.IntegerField(verbose_name='Metre Karesi')),
                ('site_icinde', models.TextField(verbose_name='Site İçinde')),
                ('tapu', models.TextField(verbose_name='Tapu Durumu')),
                ('takas', models.TextField(verbose_name='Takas')),
                ('isinma', models.TextField(verbose_name='Isınma Tipi')),
                ('kredi', models.TextField(verbose_name='Krediye Uygunluk')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Oluşturma Tarihi')),
            ],
        ),
    ]
