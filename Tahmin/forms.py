from django import forms
import pandas as pd
import os

class CreateTahminForms(forms.Form):
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'ilce.csv')   #full path to text.
    data = pd.read_csv(file_path)

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'mahalle.csv')   #full path to text.
    mahalleFile = pd.read_csv(file_path)

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'isinma.csv')   #full path to text.
    isiFile = pd.read_csv(file_path)

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'kat.xlsx')   #full path to text.
    katFile = pd.read_excel(file_path)

    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'tapu.csv')   #full path to text.
    tapuFile = pd.read_csv(file_path)

    CHOICES_ilce = []
    CHOICES_mahalle = []
    CHOICES_isinma = []
    CHOICES_kat = []
    CHOICES_tapu = []

    for i in data.ILCE:
        l = []
        l.append(i)
        l.append(i)
        CHOICES_ilce.append(l)
        
    for i in mahalleFile.MAHALLE:
        l = []
        l.append(i)
        l.append(i)
        CHOICES_mahalle.append(l)

    for i in isiFile.ISINMA:
        l = []
        l.append(i)
        l.append(i)
        CHOICES_isinma.append(l)
    for i in katFile.KAT:
        l = []
        l.append(i)
        l.append(i)
        CHOICES_kat.append(l)
    for i in tapuFile.TAPU:
        l = []
        l.append(i)
        l.append(i)
        CHOICES_tapu.append(l)

    yesOrNo = [("Evet", "Evet"),("Hayır", "Hayır")]
    istanbul = [("İstanbul", "İstanbul")]





    il = forms.ChoiceField(widget=forms.Select, label="İl", choices=istanbul)
    ilce = forms.ChoiceField(widget=forms.Select, label="İlçe", choices=CHOICES_ilce)
    mahalle = forms.ChoiceField(widget=forms.Select, label="Mahalle", choices=CHOICES_mahalle)
    oda = forms.DecimalField(label="Oda Sayısı")
    salon = forms.DecimalField(label="Salon Sayısı")
    banyo = forms.DecimalField(label="Banyo Sayısı")
    bulunan_kat = forms.ChoiceField(label="Bulunduğu Kat", widget= forms.Select, choices=CHOICES_kat)
    bina_kat = forms.DecimalField(label= "Binanın Toplam Katı")
    bina_yas = forms.DecimalField(label="Binanın Yaşı")
    site_icinde = forms.ChoiceField(label="Site İçinde", widget=forms.Select, choices=yesOrNo)
    tapu_durumu = forms.ChoiceField(label="Tapu Durumu", widget=forms.Select, choices = CHOICES_tapu)
    takas = forms.ChoiceField(label="Takas", widget=forms.Select, choices=yesOrNo)
    isinma_tipi = forms.ChoiceField(label="Isınma Tipi", widget=forms.Select, choices=CHOICES_isinma)
    kredi = forms.ChoiceField(label="Krediye uygunluk", widget=forms.Select, choices=yesOrNo)
    m2 = forms.DecimalField(label="Metre Karesi")
    

    def clean(self):
        il = self.cleaned_data.get("il")
        ilce = self.cleaned_data.get("ilce")
        mahalle = self.cleaned_data.get("mahalle")
        oda = self.cleaned_data.get("oda")
        salon = self.cleaned_data.get("salon")
        banyo = self.cleaned_data.get("banyo")
        bulunan_kat = self.cleaned_data.get("bulunan_kat")
        bina_kat = self.cleaned_data.get("bina_kat")
        bina_yas = self.cleaned_data.get("bina_yas")
        site_icinde = self.cleaned_data.get("site_icinde")
        tapu_durumu = self.cleaned_data.get("tapu_durumu")
        takas = self.cleaned_data.get("takas")
        isinma_tipi = self.cleaned_data.get("isinma_tipi")
        kredi = self.cleaned_data.get("kredi")
        m2 = self.cleaned_data.get("m2")
        
        values = {
            "il" : il,
            "ilce" : ilce,
            "mahalle" : mahalle,
            "oda" : oda,
            "salon" : salon,
            "banyo" : banyo,
            "bulunan_kat" : bulunan_kat,
            "bina_kat" : bina_kat,
            "bina_yas" : bina_yas,
            "site_icinde" : site_icinde,
            "tapu_durumu" : tapu_durumu,
            "takas" : takas,
            "isinma_tipi" : isinma_tipi,
            "kredi" : kredi,
            "m2" : m2,
        }

        return values