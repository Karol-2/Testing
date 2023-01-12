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

    def Wyslij_historie_na_mail(self, adresat, smtp_connector):
        temat = f"Wyciąg z dnia {date.today()}"
        tresc = f"Twoja historia konta Twojej firmy to: {self.historia}"
        result = smtp_connector.wyslij(temat, tresc, adresat)
        if result:
            return True
        else:
            return False
