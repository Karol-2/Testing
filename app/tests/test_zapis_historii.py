import unittest
from unittest.mock import patch, MagicMock
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

    def test_historii_ksiegowania(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.zaksieguj_przelew_przychodzacy(2000)
        konto.zaksieguj_przelew_przychodzacy(1000)
        konto.zaksieguj_przelew_wychodzacy(2000)
        self.assertEqual(konto.historia, [2000, 1000, -2000], "Zła historia dla przelewów zwykłych")

    @patch('app.KontoFirmowe.KontoFirmowe.request_do_api', return_value=True)
    def test_historii_ksiegowania_firma(self, mock):
        konto = KontoFirmowe(self.nazwa, self.nip)
        konto.zaksieguj_przelew_przychodzacy(2000)
        konto.zaksieguj_przelew_przychodzacy(1000)
        konto.zaksieguj_przelew_wychodzacy(2000)
        self.assertEqual(konto.historia, [2000, 1000, -2000], "Zla historia dla przelewów zwykłych w firmie")

    def test_historii_ksiegowania_ekspresowe(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.zaksieguj_przelew_przychodzacy(2000)
        konto.zaksieguj_przelew_przychodzacy(1000)
        konto.zaksieguj_przelew_wychodzacy(2000)
        konto.przelew_express_wychodzacy(300)
        self.assertEqual(konto.historia, [2000, 1000, -2000, -300, -1], "Zła historia dla przelewów ekspresowych")

    @patch('app.KontoFirmowe.KontoFirmowe.request_do_api', return_value=True)
    def test_historii_ksiegowania_ekspresowe_firma(self, mock):
        konto = KontoFirmowe(self.nazwa, self.nip)
        konto.zaksieguj_przelew_przychodzacy(2000)
        konto.zaksieguj_przelew_przychodzacy(1000)
        konto.zaksieguj_przelew_wychodzacy(2000)
        konto.przelew_express_wychodzacy(300)
        self.assertEqual(konto.historia, [2000, 1000, -2000, -300, -5],
                         "Zła historia dla przelewów ekspresowych w firmie")

    def test_wysyłanie_maila_z_historia(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.saldo = 1000
        konto.zaksieguj_przelew_wychodzacy(100)
        smtp_connector = SMTPConnection()
        smtp_connector.wyslij = MagicMock(return_value=True)
        status = konto.Wyslij_historie_na_mail("email@gmail.com", smtp_connector)
        self.assertTrue(status)
        smtp_connector.wyslij.assert_called_once_with(f"Wyciąg z dnia {date.today()}",
                                                      f"Historia konta: {konto.historia}", "email@gmail.com")

    @patch('app.KontoFirmowe.KontoFirmowe.czy_nip_istnieje', return_value=True)
    def test_wysyłanie_maila_z_historia_firma(self, mock_konto_firmowe):
        mock_konto_firmowe.return_value = True
        konto = KontoFirmowe(self.nazwa, self.nip)
        konto.saldo = 1000
        konto.zaksieguj_przelew_wychodzacy(100)
        smtp_connector = SMTPConnection()
        smtp_connector.wyslij = MagicMock(return_value=True)
        status = konto.Wyslij_historie_na_mail("email@gmail.com", smtp_connector)
        self.assertTrue(status)
        smtp_connector.wyslij.assert_called_once_with(f"Wyciąg z dnia {date.today()}",
                                                      f"Historia konta firmowego: {konto.historia}",
                                                      "email@gmail.com")

    def test_wysyłanie_maila_z_historia_nieudane(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.saldo = 1000
        konto.zaksieguj_przelew_wychodzacy(100)
        smtp_connector = SMTPConnection()
        smtp_connector.wyslij = MagicMock(return_value=False)
        status = konto.Wyslij_historie_na_mail("email@gmail.com", smtp_connector)
        self.assertFalse(status)
        smtp_connector.wyslij.assert_called_once_with(f"Wyciąg z dnia {date.today()}",
                                                      f"Historia konta: {konto.historia}", "email@gmail.com")

    @patch('app.KontoFirmowe.KontoFirmowe.czy_nip_istnieje', return_value=True)
    def test_wysyłanie_maila_z_historia_firma_nieudane(self, mock_konto_firmowe):
        mock_konto_firmowe.return_value = True
        konto = KontoFirmowe(self.nazwa, self.nip)
        konto.saldo = 1000
        konto.zaksieguj_przelew_wychodzacy(100)
        smtp_connector = SMTPConnection()
        smtp_connector.wyslij = MagicMock(return_value=False)
        status = konto.Wyslij_historie_na_mail("email@gmail.com", smtp_connector)
        self.assertFalse(status)
        smtp_connector.wyslij.assert_called_once_with(f"Wyciąg z dnia {date.today()}",
                                                      f"Historia konta firmowego: {konto.historia}",
                                                      "email@gmail.com")