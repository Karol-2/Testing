import unittest
from app.Konto import Konto
from app.KontoFirmowe import KontoFirmowe
from unittest.mock import patch, MagicMock


class TestKsiegowaniePrzelewow(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Mariusz"
    pesel = "68451234856"

    nazwa = "Zabka"
    nip = "765-345-12-44"

    def test_przelew_przychodzacy(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.saldo = 0
        konto.zaksieguj_przelew_przychodzacy(500)
        self.assertEqual(konto.saldo, 500, "Nie dodano pieniedzy do konta")

    def test_przelew_wychodzacy_srodki_niewystarczajace(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.saldo = 500
        konto.zaksieguj_przelew_wychodzacy(1000)
        self.assertEqual(konto.saldo, 500, "Środki na minusie")

    def test_przelew_wychodzacy(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.saldo = 500
        konto.zaksieguj_przelew_wychodzacy(100)
        self.assertEqual(konto.saldo, 500 - 100, "Środki na minusie")

    def test_seria_przelewow(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.saldo = 0
        konto.zaksieguj_przelew_przychodzacy(500)
        konto.zaksieguj_przelew_wychodzacy(100)
        konto.zaksieguj_przelew_wychodzacy(10)
        konto.zaksieguj_przelew_przychodzacy(15)
        self.assertEqual(konto.saldo, 500 - 100 - 10 + 15, "Zły stan konta po serii przelewow")

    @patch('app.KontoFirmowe.KontoFirmowe.request_do_api', return_value=True)
    def test_seria_przelewow_firma(self,mock):
        konto = KontoFirmowe(self.nazwa, self.nip)
        konto.saldo = 0
        konto.zaksieguj_przelew_przychodzacy(6000)
        konto.zaksieguj_przelew_wychodzacy(5500)
        konto.zaksieguj_przelew_wychodzacy(4000)  # tego ma nie przyjąć
        self.assertEqual(konto.saldo, 6000 - 5500, "Zły stan konta po serii przelewow")

    def test_przelew_ekspresowy_klient(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.saldo = 500
        konto.przelew_express_wychodzacy(200)
        self.assertEqual(konto.saldo, 500 - 200 - 1, "Zła wartość dla przelewu ekspresowego, klient")

    @patch('app.KontoFirmowe.KontoFirmowe.request_do_api', return_value=True)
    def test_przelew_ekspresowy_firma(self,mock):
        konto = KontoFirmowe(self.nazwa, self.nip)
        konto.saldo = 500
        konto.przelew_express_wychodzacy(200)
        self.assertEqual(konto.saldo, 500 - 200 - 5, "Zła wartość dla przelewu ekspresowego, firma")

    def test_przelew_ekspresowy_klient_na_minusie(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel)
        konto.saldo = 500
        konto.przelew_express_wychodzacy(500)
        self.assertEqual(konto.saldo, 500 - 500 - 1, "Zła wartość dla przelewu ekspresowego, klient")

    @patch('app.KontoFirmowe.KontoFirmowe.request_do_api', return_value=True)
    def test_przelew_ekspresowy_firma_na_minusie(self,mock):
        konto = KontoFirmowe(self.nazwa, self.nip)
        konto.saldo = 500
        konto.przelew_express_wychodzacy(500)
        self.assertEqual(konto.saldo, 500 - 500 - 5, "Zła wartość dla przelewu ekspresowego, firma")
