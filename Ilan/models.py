from django.db import models
from django.utils import timezone

# Create your models here.

#Ilan modelinde bulunacak değişkenler
class Ilan(models.Model):
    title = models.CharField(max_length = 500, verbose_name="Başlık")
    fiyat = models.IntegerField(verbose_name="Fiyat")
    aciklama = models.TextField(verbose_name="Açıklama")
    oda = models.IntegerField(verbose_name="Oda")
    salon = models.IntegerField(verbose_name="Salon")
    banyo = models.IntegerField(verbose_name="Banyo Sayısı")
    il = models.TextField(verbose_name="İl")
    ilçe = models.TextField(verbose_name="İlçe")
    mahalle = models.TextField(verbose_name="Mahalle")
    bina_kat = models.IntegerField(verbose_name="Binanın Kat Sayısı")
    bina_yaş = models.IntegerField(verbose_name="Binanın Yaşı")
    bulundugu_kat = models.TextField(verbose_name="Bulunduğu Kat")
    m2 = models.IntegerField(verbose_name="Metre Karesi")
    site_icinde = models.TextField(verbose_name="Site İçinde")
    tapu = models.TextField(verbose_name="Tapu Durumu")
    takas = models.TextField(verbose_name="Takas")
    isinma = models.TextField(verbose_name="Isınma Tipi")
    kredi = models.TextField(verbose_name="Krediye Uygunluk")

    created_date = models.DateTimeField(default=timezone.now,verbose_name="Oluşturma Tarihi")