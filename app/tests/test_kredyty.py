import unittest
from app.Konto import Konto
from app.KontoFirmowe import KontoFirmowe
from unittest.mock import patch
from parameterized import parameterized


class TestKredyty(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Mariusz"
    pesel = "68451234856"

    nazwa = "Zabka"
    nip = "765-345-12-44"

    @patch('app.KontoFirmowe.KontoFirmowe.request_do_api', return_value=True)
    def setUp(self,mock):
        self.konto = Konto(self.imie, self.nazwisko, self.pesel)
        self.konto_firmowe = KontoFirmowe(self.nazwa, self.nip)

    @parameterized.expand([
        ([-100, 100, 100, 100, 600], 500, True, 500),#basic przypadek
        ([], 500, False, 0), #pusta historia
        ([-100, 50], 500, False, 0),# za krótka historia
        ([-100, -200, -4555, -412, -111], 500, False, 0), # ostatnie 3 to nie wpłaty
        ([50, 30, 20, 10, 50, 10, 11], 200000, False, 0) # suma ostatnich 5 mniejsza niż kwota kredytu

    ])
    def test_Konto_Indywidualne(self, historia, kwota_kredytu, oczekiwany_wynik, oczekiwane_saldo):
        self.konto.historia = historia
        czy_przyznany = self.konto.zaciagnij_kredyt(kwota_kredytu)
        self.assertEqual(czy_przyznany, oczekiwany_wynik)
        self.assertEqual(self.konto.saldo, oczekiwane_saldo)

    @parameterized.expand([
        ([-1775, 2000, 50000], 52000, 10000, True, 62000),  # basic przypadek
        ([-1775, 4000], 4000, 2000, True, 6000),  # graniczny, przynajmniej 2x wieksze saldo
        ([-1775,-1775, 4000], 4000, 2000, True, 6000), # dwa zusy
        ([1000, 500], 1500, 500, False, 1500),  # nie płaci zusu
        ([-1775, 2000], 2000, 1700, False, 2000),  # płaci zus ale za wysoki kredyt
        ([], 500, 100, False, 500)  # brak historii
    ])
    def test_Konto_Firmowe(self, historia, saldo, kwota_kredytu, oczekiwany_wynik, oczekiwane_saldo):
        self.konto_firmowe.historia = historia
        self.konto_firmowe.saldo = saldo
        czy_przyznany = self.konto_firmowe.zaciagnij_kredyt(kwota_kredytu)
        self.assertEqual(czy_przyznany, oczekiwany_wynik)
        self.assertEqual(self.konto_firmowe.saldo, oczekiwane_saldo)
