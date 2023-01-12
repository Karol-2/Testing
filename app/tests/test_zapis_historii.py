import unittest
from unittest.mock import patch,MagicMock
from datetime import date
from app.Konto import Konto
from app.KontoFirmowe import KontoFirmowe
from app.SMTPConnection import SMTPConnection


class TestZapisHistorii(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Mariusz"
    pesel = "68451234856"

    nazwa = "Zabka"
    nip = "765-345-12-44"

    def test_zapis_historii_klient(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.zaksieguj_przelew_przychodzacy(6000)
        konto.zaksieguj_przelew_wychodzacy(5500)
        konto.zaksieguj_przelew_przychodzacy(300)
        self.assertEqual(konto.historia, [6000, -5500, 300], "Niepoprawna historia dla przelewów zwykłych, klient")

    def test_zapis_historii_ekspresowe_klient(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.zaksieguj_przelew_przychodzacy(6000)
        konto.przelew_express_wychodzacy(500)
        konto.zaksieguj_przelew_przychodzacy(300)
        self.assertEqual(konto.historia, [6000, -500, -1, 300],
                         "Niepoprawna historia dla przelewów ekspresowych, klient")

    def test_zapis_historii_firma(self):
        konto = KontoFirmowe(self.nazwa, self.nip)
        konto.zaksieguj_przelew_przychodzacy(6000)
        konto.zaksieguj_przelew_wychodzacy(5500)
        konto.zaksieguj_przelew_przychodzacy(300)
        self.assertEqual(konto.historia, [6000, -5500, 300], "Niepoprawna historia dla przelewów zwykłych, firma")

    def test_zapis_historii_ekspresowe_firma(self):
        konto = KontoFirmowe(self.nazwa, self.nip)
        konto.zaksieguj_przelew_przychodzacy(6000)
        konto.przelew_express_wychodzacy(5500)
        konto.zaksieguj_przelew_przychodzacy(300)
        self.assertEqual(konto.historia, [6000, -5500, -5, 300],
                         "Niepoprawna historia dla przelewów ekspresowych, firma")

    def test_wysylanie_maila_z_historia_konta(self):
        konto = Konto(self.imie,self.nazwisko,self.pesel)
        konto.historia = [100,200,300,400]
        smpt_connector = SMTPConnection()
        smpt_connector.wyslij = MagicMock(return_value = True)
        self.assertTrue(konto.Wyslij_historie_na_mail("email@email.com",smpt_connector))
        smpt_connector.wyslij.assert_called_once_with(f"Wyciąg z dnia {date.today()}",f"Twoja historia konta to: {konto.historia}","email@email.com")

    def test_wysylanie_maila_z_historia_konta_FAIL(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.historia = [100, 200, 300, 400]
        smpt_connector = SMTPConnection()
        smpt_connector.wyslij = MagicMock(return_value=False)
        self.assertFalse(konto.Wyslij_historie_na_mail("email@email.com", smpt_connector))

    def test_wysylanie_maila_z_historia_konto_firmowe(self):
        konto = KontoFirmowe(self.nazwa,self.nip)
        konto.historia = [100,200,300,400]
        smpt_connector = SMTPConnection()
        smpt_connector.wyslij = MagicMock(return_value = True)
        self.assertTrue(konto.Wyslij_historie_na_mail("email@email.com",smpt_connector))
        smpt_connector.wyslij.assert_called_once_with(f"Wyciąg z dnia {date.today()}",f"Twoja historia konta Twojej firmy to: {konto.historia}","email@email.com")

    def test_wysylanie_maila_z_historia_konto_firmowe_FAIL(self):
        konto = KontoFirmowe(self.nazwa, self.nip)
        konto.historia = [100, 200, 300, 400]
        smpt_connector = SMTPConnection()
        smpt_connector.wyslij = MagicMock(return_value=False)
        self.assertFalse(konto.Wyslij_historie_na_mail("email@email.com", smpt_connector))

