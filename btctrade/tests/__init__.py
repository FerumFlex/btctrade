from unittest import TestCase


import btctrade


class TestBtctrade(TestCase):
    def test_public(self):
        trade = btctrade.Btctrade()
        self.assertTrue(trade.get_deals('btc_uah'))
        self.assertTrue(trade.get_sell_trades('btc_uah'))
        self.assertTrue(trade.get_buy_trades('btc_uah'))
        self.assertTrue(trade.get_japan_stats('btc_uah'))
