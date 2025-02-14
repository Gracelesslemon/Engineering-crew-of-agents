import unittest
import datetime
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account(account_id="123")

    def test_init(self):
        self.assertEqual(self.account.account_id, "123")
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(len(self.account.transactions), 0)
        self.assertEqual(self.account.initial_deposit, 0.0)
        self.assertIsInstance(self.account.creation_timestamp, datetime.datetime)

    def test_deposit(self):
        self.assertTrue(self.account.deposit(100.0))
        self.assertEqual(self.account.balance, 100.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]['type'], 'deposit')
        self.assertEqual(self.account.transactions[0]['amount'], 100.0)
        self.assertEqual(self.account.initial_deposit, 100.0)

        self.assertFalse(self.account.deposit(-50.0))
        self.assertEqual(self.account.balance, 100.0)
        self.assertEqual(len(self.account.transactions), 1)

    def test_withdraw(self):
        self.account.deposit(100.0)
        self.assertTrue(self.account.withdraw(50.0))
        self.assertEqual(self.account.balance, 50.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'withdraw')
        self.assertEqual(self.account.transactions[1]['amount'], 50.0)

        self.assertFalse(self.account.withdraw(150.0))
        self.assertEqual(self.account.balance, 50.0)
        self.assertEqual(len(self.account.transactions), 2)

    def test_buy_shares(self):
        self.account.deposit(10000.0)
        self.assertTrue(self.account.buy_shares("AAPL", 10))
        self.assertEqual(self.account.balance, 8300.0)
        self.assertEqual(self.account.holdings, {"AAPL": 10})
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'buy')
        self.assertEqual(self.account.transactions[1]['symbol'], 'AAPL')
        self.assertEqual(self.account.transactions[1]['quantity'], 10)
        self.assertEqual(self.account.transactions[1]['price'], 170.0)

        self.assertFalse(self.account.buy_shares("AAPL", 100))
        self.assertEqual(self.account.balance, 8300.0)
        self.assertEqual(self.account.holdings, {"AAPL": 10})
        self.assertEqual(len(self.account.transactions), 2)

        self.assertFalse(self.account.buy_shares("AAPL", -1))

    def test_sell_shares(self):
        self.account.deposit(10000.0)
        self.account.buy_shares("AAPL", 10)
        self.assertTrue(self.account.sell_shares("AAPL", 5))
        self.assertEqual(self.account.balance, 9150.0)
        self.assertEqual(self.account.holdings, {"AAPL": 5})
        self.assertEqual(len(self.account.transactions), 3)
        self.assertEqual(self.account.transactions[2]['type'], 'sell')
        self.assertEqual(self.account.transactions[2]['symbol'], 'AAPL')
        self.assertEqual(self.account.transactions[2]['quantity'], 5)
        self.assertEqual(self.account.transactions[2]['price'], 170.0)

        self.assertTrue(self.account.sell_shares("AAPL", 5))
        self.assertEqual(self.account.balance, 10000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(len(self.account.transactions), 4)

        self.assertFalse(self.account.sell_shares("AAPL", 1))

        self.assertFalse(self.account.sell_shares("TSLA", 1))

        self.account.buy_shares("AAPL", 10)
        self.assertFalse(self.account.sell_shares("AAPL", -1))

    def test_get_balance(self):
        self.account.deposit(100.0)
        self.assertEqual(self.account.get_balance(), 100.0)

    def test_get_holdings(self):
        self.account.buy_shares("AAPL", 5)
        self.assertEqual(self.account.get_holdings(), {"AAPL": 5})

    def test_get_portfolio_value(self):
        self.account.deposit(10000.0)
        self.account.buy_shares("AAPL", 10)
        self.account.buy_shares("TSLA", 1)
        self.assertEqual(self.account.get_portfolio_value(), 9700.0 + 170.0 * 10 + 800.0)

    def test_get_profit_loss(self):
        self.account.deposit(10000.0)
        self.account.buy_shares("AAPL", 10)
        self.assertEqual(self.account.get_profit_loss(), -1700.0)

        self.account.sell_shares("AAPL", 5)
        self.assertEqual(self.account.get_profit_loss(), -850.0)

        self.account.sell_shares("AAPL", 5)
        self.assertEqual(self.account.get_profit_loss(), 0.0)

        self.assertEqual(self.account.initial_deposit, 10000.0)

        account2 = Account("456")
        self.assertEqual(account2.get_profit_loss(), 0.0)

    def test_get_transactions(self):
        self.account.deposit(100.0)
        self.account.withdraw(50.0)
        self.assertEqual(len(self.account.get_transactions()), 2)

    def test_get_share_price(self):
        self.assertEqual(get_share_price("AAPL"), 170.0)
        self.assertEqual(get_share_price("TSLA"), 800.0)
        self.assertEqual(get_share_price("GOOGL"), 2600.0)
        self.assertEqual(get_share_price("MSFT"), 100.0)
