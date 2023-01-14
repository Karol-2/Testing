import os
import requests
from datetime import date

from app.Konto import Konto


class KontoFirmowe(Konto):
    def __init__(self, nazwa, nip):
        self.nazwa = nazwa
        self.saldo = 0
        self.historia = []
        self.oplata_za_ekspres = 5
        self.SprawdzanieNIP(nip)
        self.czy_nip_istnieje(nip)

    def SprawdzanieNIP(self, NIP):
        if sum(a.isdigit() for a in NIP) == 10:
            if self.czy_nip_istnieje(NIP) is None:
                self.nip = "Pranie!"
            else:
                self.nip = NIP
        else:
            self.nip = "Niepoprawny NIP!"

    def zaciagnij_kredyt(self, kwota):
        if -1775 in self.historia and self.saldo >= kwota * 2:
            self.zaksieguj_przelew_przychodzacy(kwota)
            return True
        return False

    def Wyslij_historie_na_mail(self, adresat, smtp_connector):
        temat = f"Wyciąg z dnia {date.today()}"
        tresc = f"Historia konta firmowego: {self.historia}"
        result = smtp_connector.wyslij(temat, tresc, adresat)
        if result:
            return True
        else:
            return False

    @classmethod
    def czy_nip_istnieje(cls, nip):
        gov_url = os.getenv('BANK_APP_MF_URL', 'https://wl-test.mf.gov.pl/')
        data = date.today()
        url = f"{gov_url}api/search/nip/{nip}?date={data}"
        return cls.request_do_api(url)

    @classmethod
    def request_do_api(cls, url):
        return requests.get(url).status_code == 200