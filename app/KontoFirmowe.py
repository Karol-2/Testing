import os
import requests
from datetime import  date

from app.Konto import Konto


class KontoFirmowe(Konto):
    def __init__(self, nazwa, nip):
        self.nazwa = nazwa
        self.saldo = 0
        self.historia = []
        self.oplata_za_ekspres = 5
        self.SprawdzanieNIP(nip)

    def SprawdzanieNIP(self, NIP):
        if sum(a.isdigit() for a in NIP) == 10:
            self.nip = NIP
        else:
            self.nip = "Niepoprawny NIP!"

    def zaciagnij_kredyt(self, kwota):
        if -1775 in self.historia and self.saldo >= kwota * 2:
            self.zaksieguj_przelew_przychodzacy(kwota)
            return True
        return False

    @classmethod
    def czy_nip_istnieje(cls,nip):
        gov_url = os.getenv('BANK_APP_MF_URL',"https://wl-test.mf.gov.pl/")
        data = date.today()
        url =f"{gov_url}api/search/nip/{nip}?date={data}"
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            cls.nip="PRANIE!!!"