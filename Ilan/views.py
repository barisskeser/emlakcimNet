from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Ilan
import pandas as pd
import os

from django.urls import reverse

from .forms import CreateForms
from django.http import Http404

# Create your views here.

#Anasayfaya ait fonksiyon
def index(request):
    if request.method == "GET":
        keyword = request.GET.get('keyword')
        if keyword: # Eğer arama yapılırsa ilan başlığına göre ilan listesine yönlendirme
            posts = Ilan.objects.all().filter(title__contains = keyword).order_by("created_date") #başıkta keyword değerini içeren ilanların getirilmesi
            return HttpResponseRedirect("/ilan-list/?keyword=" + keyword)
    return render(request, "index.html") #Html dosyasının çağrılması

def create(request):

    if request.method == "GET":
        keyword = request.GET.get('keyword')
        if keyword:# Eğer arama yapılırsa ilan başlığına göre ilan listesine yönlendirme
            posts = Ilan.objects.all().filter(title__contains = keyword).order_by("created_date")
            return HttpResponseRedirect("/ilan-list/?keyword=" + keyword) 

    #HTML inputta girilen değerlerin forms.py de ki CreateForms a gönderilerek nesne oluşturulması
    if request.method == "POST":
        form = CreateForms(request.POST)
        print(form.errors)
        # Eğer veriler geçerli ise değişkenlere aktarılması
        if form.is_valid():
            title = form.cleaned_data.get("title")
            il = form.cleaned_data.get("il")
            ilce = form.cleaned_data.get("ilce")
            mahalle = form.cleaned_data.get("mahalle")
            oda = form.cleaned_data.get("oda")
            salon = form.cleaned_data.get("salon")
            banyo = form.cleaned_data.get("banyo")
            bulunan_kat = form.cleaned_data.get("bulunan_kat")
            bina_kat = form.cleaned_data.get("bina_kat")
            bina_yas = form.cleaned_data.get("bina_yas")
            site_icinde = form.cleaned_data.get("site_icinde")
            tapu_durumu = form.cleaned_data.get("tapu_durumu")
            takas = form.cleaned_data.get("takas")
            isinma_tipi = form.cleaned_data.get("isinma_tipi")
            kredi = form.cleaned_data.get("kredi")
            m2 = form.cleaned_data.get("m2")
            fiyat = form.cleaned_data.get("fiyat")
            aciklama = form.cleaned_data.get("aciklama")

            #Ilan nesnesi oluşturulması
            ilan = Ilan(title = title, 
            fiyat = fiyat, 
            aciklama = aciklama, 
            oda = oda, 
            salon = salon, 
            banyo = banyo, 
            il = il,
            ilçe = ilce, 
            mahalle = mahalle, 
            bina_kat = bina_kat, 
            bina_yaş = bina_yas, 
            bulundugu_kat = bulunan_kat,
            site_icinde = site_icinde,
            tapu = tapu_durumu,
            takas= takas,
            isinma = isinma_tipi,
            kredi=kredi,
            m2 = m2)

            #Kaydedilmesi
            ilan.save()
            return HttpResponseRedirect('/ilan-list') #İlan listesine yönderilme
        else:
            raise Http404
    
    #mahalle.csv dosyasının okunarak html'e gönderilmesi
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'mahalle.csv')
    mahalle = pd.read_csv(file_path)

    form = CreateForms()
    return render(request, "create-ilan.html", {'form' : form, "mahalle" : mahalle, "len_mahalle" : range(778)}) #Html dosyasının çağrılması ve veri gönderilmesi

def ilan(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        if keyword:# Eğer arama yapılırsa ilan başlığına göre ilan listesine yönlendirme
            posts = Ilan.objects.all().filter(title__contains = keyword).order_by("created_date")
            return render(request, 'ilan-list.html', {'posts': posts})
    
    posts = Ilan.objects.order_by("created_date").all()
    return render(request, "ilan-list.html", {'posts' : posts}) #Html dosyasının çağrılması ve veri gönderilmesi


def detail(request, id):
    if request.method == "GET":
        keyword = request.GET.get('keyword')
        if keyword:# Eğer arama yapılırsa ilan başlığına göre ilan listesine yönlendirme
            posts = Ilan.objects.all().filter(title__contains = keyword).order_by("created_date")
            return HttpResponseRedirect("/ilan-list/?keyword=" + keyword)
    post = Ilan.objects.get(id = id)
    return render(request, "detail.html", {'post' : post}) #Html dosyasının çağrılması ve veri gönderilmesi