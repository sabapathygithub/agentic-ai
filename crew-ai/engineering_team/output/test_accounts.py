import unittest
from accounts import Account, get_share_price


class TestGetSharePrice(unittest.TestCase):
    def test_get_price_aapl(self):
        self.assertEqual(get_share_price("AAPL"), 150.0)
    
    def test_get_price_tsla(self):
        self.assertEqual(get_share_price("TSLA"), 200.0)
    
    def test_get_price_googl(self):
        self.assertEqual(get_share_price("GOOGL"), 100.0)
    
    def test_get_price_invalid_symbol(self):
        with self.assertRaises(ValueError) as context:
            get_share_price("INVALID")
        self.assertIn("Price not available for symbol", str(context.exception))


class TestAccountInitialization(unittest.TestCase):
    def test_account_creation(self):
        account = Account("testuser")
        self.assertEqual(account.username, "testuser")
        self.assertEqual(account.balance, 0.0)
        self.assertEqual(account.holdings, {})
        self.assertEqual(account.transactions, [])
        self.assertEqual(account._total_deposited, 0.0)


class TestAccountDeposit(unittest.TestCase):
    def setUp(self):
        self.account = Account("testuser")
    
    def test_deposit_positive_amount(self):
        self.account.deposit(1000.0)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account._total_deposited, 1000.0)
    
    def test_deposit_multiple_times(self):
        self.account.deposit(500.0)
        self.account.deposit(300.0)
        self.assertEqual(self.account.balance, 800.0)
        self.assertEqual(self.account._total_deposited, 800.0)
    
    def test_deposit_zero(self):
        self.account.deposit(0.0)
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(self.account._total_deposited, 0.0)
    
    def test_deposit_negative_amount(self):
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-100.0)
        self.assertIn("cannot be negative", str(context.exception))
    
    def test_deposit_transaction_recorded(self):
        self.account.deposit(1000.0)
        self.assertEqual(len(self.account.transactions), 1)
        transaction = self.account.transactions[0]
        self.assertEqual(transaction["type"], "deposit")
        self.assertEqual(transaction["amount"], 1000.0)
        self.assertEqual(transaction["balance"], 1000.0)


class TestAccountWithdrawal(unittest.TestCase):
    def setUp(self):
        self.account = Account("testuser")
        self.account.deposit(1000.0)
    
    def test_withdraw_valid_amount(self):
        self.account.withdraw(300.0)
        self.assertEqual(self.account.balance, 700.0)
    
    def test_withdraw_entire_balance(self):
        self.account.withdraw(1000.0)
        self.assertEqual(self.account.balance, 0.0)
    
    def test_withdraw_negative_amount(self):
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-100.0)
        self.assertIn("cannot be negative", str(context.exception))
    
    def test_withdraw_exceeds_balance(self):
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(1500.0)
        self.assertIn("Insufficient funds", str(context.exception))
    
    def test_withdraw_transaction_recorded(self):
        self.account.withdraw(300.0)
        self.assertEqual(len(self.account.transactions), 2)
        transaction = self.account.transactions[1]
        self.assertEqual(transaction["type"], "withdrawal")
        self.assertEqual(transaction["amount"], 300.0)
        self.assertEqual(transaction["balance"], 700.0)


class TestAccountBuyShares(unittest.TestCase):
    def setUp(self):
        self.account = Account("testuser")
        self.account.deposit(10000.0)
    
    def test_buy_shares_valid(self):
        self.account.buy_shares("AAPL", 10)
        self.assertEqual(self.account.holdings["AAPL"], 10)
        self.assertEqual(self.account.balance, 10000.0 - (150.0 * 10))
    
    def test_buy_shares_multiple_symbols(self):
        self.account.buy_shares("AAPL", 5)
        self.account.buy_shares("TSLA", 3)
        self.assertEqual(self.account.holdings["AAPL"], 5)
        self.assertEqual(self.account.holdings["TSLA"], 3)
    
    def test_buy_shares_same_symbol_multiple_times(self):
        self.account.buy_shares("AAPL", 5)
        self.account.buy_shares("AAPL", 3)
        self.assertEqual(self.account.holdings["AAPL"], 8)
    
    def test_buy_shares_zero_quantity(self):
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares("AAPL", 0)
        self.assertIn("must be positive", str(context.exception))
    
    def test_buy_shares_negative_quantity(self):
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares("AAPL", -5)
        self.assertIn("must be positive", str(context.exception))
    
    def test_buy_shares_insufficient_funds(self):
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares("AAPL", 100)
        self.assertIn("Insufficient funds", str(context.exception))
    
    def test_buy_shares_invalid_symbol(self):
        with self.assertRaises(ValueError):
            self.account.buy_shares("INVALID", 5)
    
    def test_buy_shares_transaction_recorded(self):
        self.account.buy_shares("AAPL", 10)
        self.assertEqual(len(self.account.transactions), 2)
        transaction = self.account.transactions[1]
        self.assertEqual(transaction["type"], "buy")
        self.assertEqual(transaction["symbol"], "AAPL")
        self.assertEqual(transaction["quantity"], 10)
        self.assertEqual(transaction["price"], 150.0)
        self.assertEqual(transaction["total"], 1500.0)


class TestAccountSellShares(unittest.TestCase):
    def setUp(self):
        self.account = Account("testuser")
        self.account.deposit(10000.0)
        self.account.buy_shares("AAPL", 20)
        self.account.buy_shares("TSLA", 10)
    
    def test_sell_shares_valid(self):
        initial_balance = self.account.balance
        self.account.sell_shares("AAPL", 5)
        self.assertEqual(self.account.holdings["AAPL"], 15)
        self.assertEqual(self.account.balance, initial_balance + (150.0 * 5))
    
    def test_sell_all_shares(self):
        self.account.sell_shares("AAPL", 20)
        self.assertNotIn("AAPL", self.account.holdings)
    
    def test_sell_shares_zero_quantity(self):
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares("AAPL", 0)
        self.assertIn("must be positive", str(context.exception))
    
    def test_sell_shares_negative_quantity(self):
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares("AAPL", -5)
        self.assertIn("must be positive", str(context.exception))
    
    def test_sell_shares_insufficient_holdings(self):
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares("AAPL", 25)
        self.assertIn("Insufficient shares", str(context.exception))
    
    def test_sell_shares_not_owned(self):
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares("GOOGL", 5)
        self.assertIn("Insufficient shares", str(context.exception))
    
    def test_sell_shares_transaction_recorded(self):
        self.account.sell_shares("AAPL", 5)
        self.assertEqual(len(self.account.transactions), 4)
        transaction = self.account.transactions[3]
        self.assertEqual(transaction["type"], "sell")
        self.assertEqual(transaction["symbol"], "AAPL")
        self.assertEqual(transaction["quantity"], 5)
        self.assertEqual(transaction["price"], 150.0)
        self.assertEqual(transaction["total"], 750.0)


class TestAccountPortfolioValue(unittest.TestCase):
    def test_portfolio_value_cash_only(self):
        account = Account("testuser")
        account.deposit(5000.0)
        self.assertEqual(account.calculate_portfolio_value(), 5000.0)
    
    def test_portfolio_value_with_holdings(self):
        account = Account("testuser")
        account.deposit(10000.0)
        account.buy_shares("AAPL", 10)
        account.buy_shares("TSLA", 5)
        self.assertEqual(account.calculate_portfolio_value(), 10000.0)
    
    def test_portfolio_value_empty_account(self):
        account = Account("testuser")
        self.assertEqual(account.calculate_portfolio_value(), 0.0)


class TestAccountProfitLoss(unittest.TestCase):
    def test_profit_loss_no_change(self):
        account = Account("testuser")
        account.deposit(5000.0)
        self.assertEqual(account.calculate_profit_loss(), 0.0)
    
    def test_profit_loss_with_holdings(self):
        account = Account("testuser")
        account.deposit(10000.0)
        account.buy_shares("AAPL", 20)
        self.assertEqual(account.calculate_profit_loss(), 0.0)
    
    def test_profit_loss_after_withdrawal(self):
        account = Account("testuser")
        account.deposit(5000.0)
        account.withdraw(1000.0)
        self.assertEqual(account.calculate_profit_loss(), -1000.0)
    
    def test_profit_loss_empty_account(self):
        account = Account("testuser")
        self.assertEqual(account.calculate_profit_loss(), 0.0)


class TestAccountGetters(unittest.TestCase):
    def setUp(self):
        self.account = Account("testuser")
        self.account.deposit(5000.0)
        self.account.buy_shares("AAPL", 10)
    
    def test_get_holdings(self):
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {"AAPL": 10})
        holdings["AAPL"] = 999
        self.assertEqual(self.account.holdings["AAPL"], 10)
    
    def test_get_transactions(self):
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 2)
        transactions.append({"type": "fake"})
        self.assertEqual(len(self.account.transactions), 2)


class TestAccountComplexScenarios(unittest.TestCase):
    def test_multiple_operations(self):
        account = Account("trader1")
        account.deposit(20000.0)
        account.buy_shares("AAPL", 50)
        account.buy_shares("TSLA", 25)
        account.sell_shares("AAPL", 10)
        account.withdraw(1000.0)
        
        self.assertEqual(account.holdings["AAPL"], 40)
        self.assertEqual(account.holdings["TSLA"], 25)
        expected_balance = 20000.0 - (50*150.0) - (25*200.0) + (10*150.0) - 1000.0
        self.assertEqual(account.balance, expected_balance)
    
    def test_trading_cycle(self):
        account = Account("trader2")
        account.deposit(5000.0)
        account.buy_shares("GOOGL", 20)
        account.sell_shares("GOOGL", 20)
        
        self.assertEqual(len(account.holdings), 0)
        self.assertEqual(account.balance, 5000.0)
        self.assertEqual(account.calculate_profit_loss(), 0.0)
    
    def test_edge_case_exact_balance(self):
        account = Account("trader3")
        account.deposit(1500.0)
        account.buy_shares("AAPL", 10)
        
        self.assertEqual(account.balance, 0.0)
        self.assertEqual(account.holdings["AAPL"], 10)


if __name__ == "__main__":
    unittest.main()