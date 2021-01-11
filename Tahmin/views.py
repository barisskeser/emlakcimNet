from django.shortcuts import render, redirect, HttpResponseRedirect
import pandas as pd
import numpy
import os
import pickle

from scipy import stats
from pandas import Series
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
import xgboost as xgb

from django.urls import reverse
from django.http import Http404

from .models import Tahmin
from .forms import CreateTahminForms
from Ilan.models import Ilan

# Create your views here.

#Tahmin verilerinin girildiği sayfaya ait fonksiyon
def create(request):
    
    if request.method == "GET":
        keyword = request.GET.get('keyword')
        if keyword: # Eğer arama yapılırsa ilan başlığına göre ilan listesine yönlendirme
            posts = Ilan.objects.all().filter(title__contains = keyword).order_by("created_date")
            return HttpResponseRedirect("/ilan-list/?keyword=" + keyword)
    
    #HTML inputta girilen değerlerin forms.py de ki CreateTahminForms a gönderilerek nesne oluşturulması
    if request.method == "POST":
        form = CreateTahminForms(request.POST)
        print(form.errors)
        # Eğer veriler geçerli ise değişkenlere aktarılması
        if form.is_valid():
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

            #Ilan nesnesi oluşturulması
            tahmin = Tahmin(
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
            tahmin.save()

            last = Tahmin.objects.last() #eklenen Tahmin verilerinin alınması
            return HttpResponseRedirect("/tahmin/show/" + str(last.id)) # İd ile birlikte Tahmin görüntülemeye yönderilme
        else:
            raise Http404


    # mahalle.csv okunması
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'mahalle.csv')  
    mahalle = pd.read_csv(file_path)

    form = CreateTahminForms()
    return render(request, "create-tahmin.html", {'form' : form, "mahalle" : mahalle, "len_mahalle" : range(778)}) #Html dosyasının çağrılması ve veri gönderilmesi

def show(request, id):

    if request.method == "GET":
        keyword = request.GET.get('keyword')
        if keyword: # Eğer arama yapılırsa ilan başlığına göre ilan listesine yönlendirme
            posts = Ilan.objects.all().filter(title__contains = keyword).order_by("created_date")
            return HttpResponseRedirect("/ilan-list/?keyword=" + keyword)

    # XGBR modelinin nesneye aktarılması
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'xgbr.dat')   
    loaded_model = pickle.load(open(file_path, "rb"))
    
    #Değerlerin tahminde kullanılan değerlere göre karşılıklarının bulunduğu dosyalar. Label encode karşılıkları
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'kat.xlsx')   
    kat = pd.read_excel(file_path)

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'mahalle.csv')   
    mahalle = pd.read_csv(file_path)

    #Label encode karşılıkları
    tapuEncode = {
        "Kat Mülkiyeti" : 0,
        "Kat İrtifakı" : 1,
        "Arsa" : 2
    }

    isinmaEncode = {
        'Kombi':0,
        'Merkezi':1,
        'Kat Kaloriferi':2,
        'Jeotermal Isıtma':3,
        'Belirtilmemiş':4,
        'Isıtma Yok':5,
        'Soba':6,
        'Klima':7,
        'Güneş Enerjisi':8
    }

    tahmin = Tahmin.objects.get(id = id) # Tahmin verilerinin getirilmesi

    zipcode = None
    katEncode = None

    #Tahmin için değerlerin alınması
    for i in range(len(mahalle)):
        if mahalle.MAHALLE[i] == tahmin.mahalle and mahalle.İLCE[i] == tahmin.ilçe:
            zipcode = mahalle.ZIPCODE[i]

    for i in range(37):
        if kat.KAT[i] == tahmin.bulundugu_kat:
            katEncode = kat.ENCODE[i]
    
    site = None
    if tahmin.site_icinde == "Evet":
        site = 1
    else:
        site = 0

    takas = None
    if tahmin.takas == "Evet":
        takas = 1
    else:
        takas = 0
        
    kredi = None
    if tahmin.kredi == "Evet":
        kredi = 1
    else:
        kredi = 0
    
    #Tahmin için dizi oluşturma
    X = [
        tahmin.banyo,
        tahmin.bina_kat,
        tahmin.bina_yaş,
        katEncode,
        tahmin.m2,
        zipcode,
        tahmin.oda,
        tahmin.salon,
        site,
        tapuEncode[tahmin.tapu],
        takas,
        isinmaEncode[tahmin.isinma],
        kredi
    ]
    # X değeri üzerinde yapılan işlemler
    X_np = numpy.array(X).reshape(-1,1)
    X_DataFrame = pd.DataFrame(X_np.T)
    X_DataFrame=pd.get_dummies(X_DataFrame,drop_first=True)
    X_DataFrame=X_DataFrame.assign(const=1)


    yeni = numpy.array(X_DataFrame.iloc[0]).reshape(-1,1).T


    pred = loaded_model.predict(yeni) # Tahmin üretilmesi
    
    #int e dönüştürme
    fiyat = int(pred[0] // 1)

    #Sayıyı yuvarlayarak alt ve üst sınırlar oluşturma işlemi
    # %10 az ve fazla
    alt_fiyat = fiyat - fiyat * 0.1
    ust_fiyat = fiyat + fiyat * 0.1

    left_alt = alt_fiyat // 1000
    right_alt = alt_fiyat % 1000
    
    left_ust = ust_fiyat // 1000
    right_ust = ust_fiyat % 1000

    if right_alt < 500:
        alt_fiyat = left_alt * 1000
    else:
        alt_fiyat = (left_alt + 1) * 1000

    if right_ust < 500:
        ust_fiyat = left_ust * 1000
    else:
        ust_fiyat = (left_ust + 1) * 1000

    #Bilgilerin html dosyasına gönderilmesi ve html dosyasının çağrılması
    return render(request, "tahmin-show.html", {'tahmin' : tahmin, "alt_fiyat" : int(alt_fiyat), "ust_fiyat" : int(ust_fiyat), "pred" : fiyat})

def register(request, id):

    tahmin = Tahmin.objects.get(id = id) #tahmin değerlerinin getirilmesi

    if request.method == "GET":
        keyword = request.GET.get('keyword')
        if keyword: # Eğer arama yapılırsa ilan başlığına göre ilan listesine yönlendirme
            posts = Ilan.objects.all().filter(title__contains = keyword).order_by("created_date")
            return HttpResponseRedirect("/ilan-list/?keyword=" + keyword)
    
    #Girilen değerlere göre ilan oluşturma
    if request.method == "POST":
        fiyat = request.POST.get("fiyat")
        title = request.POST.get("title")
        aciklama = request.POST.get("aciklama")

        ilan = Ilan(title = title, 
        fiyat = fiyat, 
        aciklama = aciklama, 
        oda = tahmin.oda, 
        salon = tahmin.salon, 
        banyo = tahmin.banyo, 
        il = tahmin.il,
        ilçe = tahmin.ilçe, 
        mahalle = tahmin.mahalle, 
        bina_kat = tahmin.bina_kat, 
        bina_yaş = tahmin.bina_yaş, 
        bulundugu_kat = tahmin.bulundugu_kat,
        site_icinde = tahmin.site_icinde,
        tapu = tahmin.tapu,
        takas= tahmin.takas,
        isinma = tahmin.isinma,
        kredi= tahmin.kredi,
        m2 = tahmin.m2)

        #İlanın kaydedilmesi
        ilan.save()

        #İlan listesine yönlendirme
        return HttpResponseRedirect('/ilan-list')

    return render(request, "tahmin-register.html", {'tahmin' : tahmin}) #tahmin değerinin html'e gönderilmesi ve html dosyasının çağrılması