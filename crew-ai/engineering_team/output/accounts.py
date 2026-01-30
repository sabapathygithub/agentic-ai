# accounts.py - Account Management System for Trading Simulation Platform

def get_share_price(symbol: str) -> float:
    """Returns the current price of a share for testing purposes.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'TSLA', 'GOOGL')
        
    Returns:
        Current price of the share
        
    Raises:
        ValueError: If symbol is not supported
    """
    prices = {
        'AAPL': 150.0,
        'TSLA': 200.0,
        'GOOGL': 100.0
    }
    
    if symbol not in prices:
        raise ValueError(f"Price not available for symbol: {symbol}")
    
    return prices[symbol]


class Account:
    """Account management system for trading simulation platform."""
    
    def __init__(self, username: str):
        """Initializes a new account with the specified username.
        
        Args:
            username: Unique identifier for the user account
        """
        self.username = username
        self.balance = 0.0
        self.holdings = {}  # symbol -> quantity
        self.transactions = []  # list of transaction records
        self._total_deposited = 0.0  # track total deposits for profit/loss calculation
    
    def deposit(self, amount: float) -> None:
        """Deposits funds into the account.
        
        Args:
            amount: Amount to deposit
            
        Raises:
            ValueError: If amount is negative
        """
        if amount < 0:
            raise ValueError("Deposit amount cannot be negative")
        
        self.balance += amount
        self._total_deposited += amount
        self.transactions.append({
            'type': 'deposit',
            'amount': amount,
            'balance': self.balance
        })
    
    def withdraw(self, amount: float) -> None:
        """Withdraws funds from the account.
        
        Args:
            amount: Amount to withdraw
            
        Raises:
            ValueError: If amount is negative or exceeds available balance
        """
        if amount < 0:
            raise ValueError("Withdrawal amount cannot be negative")
        
        if amount > self.balance:
            raise ValueError(f"Insufficient funds. Available balance: {self.balance}")
        
        self.balance -= amount
        self.transactions.append({
            'type': 'withdrawal',
            'amount': amount,
            'balance': self.balance
        })
    
    def buy_shares(self, symbol: str, quantity: int) -> None:
        """Buys a specified quantity of shares.
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares to buy
            
        Raises:
            ValueError: If purchase is not possible (insufficient funds or invalid quantity)
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        
        if total_cost > self.balance:
            raise ValueError(f"Insufficient funds. Cost: {total_cost}, Available: {self.balance}")
        
        self.balance -= total_cost
        
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        self.transactions.append({
            'type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'price': share_price,
            'total': total_cost,
            'balance': self.balance
        })
    
    def sell_shares(self, symbol: str, quantity: int) -> None:
        """Sells a specified quantity of shares.
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares to sell
            
        Raises:
            ValueError: If sale is not possible (insufficient shares or invalid quantity)
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            current_holdings = self.holdings.get(symbol, 0)
            raise ValueError(f"Insufficient shares. You own {current_holdings} shares of {symbol}")
        
        share_price = get_share_price(symbol)
        total_revenue = share_price * quantity
        
        self.balance += total_revenue
        self.holdings[symbol] -= quantity
        
        # Remove symbol from holdings if quantity reaches zero
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        self.transactions.append({
            'type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'price': share_price,
            'total': total_revenue,
            'balance': self.balance
        })
    
    def calculate_portfolio_value(self) -> float:
        """Calculates the total value of the user's portfolio.
        
        Returns:
            Total portfolio value (cash + current value of all holdings)
        """
        holdings_value = 0.0
        
        for symbol, quantity in self.holdings.items():
            share_price = get_share_price(symbol)
            holdings_value += share_price * quantity
        
        return self.balance + holdings_value
    
    def calculate_profit_loss(self) -> float:
        """Calculates profit or loss since initial deposits.
        
        Returns:
            Profit (positive) or loss (negative) amount
        """
        current_value = self.calculate_portfolio_value()
        return current_value - self._total_deposited
    
    def get_holdings(self) -> dict:
        """Returns current holdings.
        
        Returns:
            Dictionary mapping symbols to quantities
        """
        return self.holdings.copy()
    
    def get_transactions(self) -> list:
        """Returns all transactions.
        
        Returns:
            List of transaction records
        """
        return self.transactions.copy()