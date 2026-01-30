# Detailed Design for the `accounts.py` Module

The `accounts.py` module is designed to simulate an account management system for a trading simulation platform. Below is a detailed outline of the classes and methods included in the module, describing their functionality:

## Class: `Account`

This is the main class responsible for managing user accounts, transactions, and portfolio calculations.

### Attributes:

- **`username`**: `str` - Unique identifier for the user account.
- **`balance`**: `float` - Available cash balance in the account.
- **`holdings`**: `dict` - Dictionary of the user's current share holdings, mapping symbols to quantities.
- **`transactions`**: `list` - List of transactions made by the user.

### Methods:

- **`__init__(self, username: str)`**:
  - Initializes a new account with the specified username and a zero balance.
- **`deposit(self, amount: float) -> None`**:
  - Deposits a specified amount of funds into the account.
  - Raises `ValueError` if the amount is negative.

- **`withdraw(self, amount: float) -> None`**:
  - Withdraws a specified amount of funds from the account.
  - Raises `ValueError` if the amount is negative or exceeds available balance.

- **`buy_shares(self, symbol: str, quantity: int) -> None`**:
  - Buys a specified quantity of shares for the given symbol.
  - Uses `get_share_price(symbol)` to determine the cost.
  - Ensures the user has enough balance to make the purchase.
  - Raises `ValueError` if the purchase is not possible.

- **`sell_shares(self, symbol: str, quantity: int) -> None`**:
  - Sells a specified quantity of shares for the given symbol.
  - Uses `get_share_price(symbol)` to determine the revenue.
  - Ensures the user owns enough of the shares to sell.
  - Raises `ValueError` if the sale is not possible.

- **`calculate_portfolio_value(self) -> float`**:
  - Calculates and returns the total value of the user's portfolio based on current share prices.

- **`calculate_profit_loss(self) -> float`**:
  - Calculates and returns the profit or loss since the initial deposit.

- **`get_holdings(self) -> dict`**:
  - Returns a dictionary of current holdings with symbols as keys and quantities as values.

- **`get_transactions(self) -> list`**:
  - Returns a list of all transactions made by the user.

### External Function:

- **`get_share_price(symbol: str) -> float`**:
  - Provided external function to get the current price of a share. For testing purposes, returns fixed prices for `AAPL`, `TSLA`, and `GOOGL`.

### Example of usage:

```python
# Create an account
account = Account("john_doe")

# Deposit funds
account.deposit(1000.0)

# Buy some shares
account.buy_shares("AAPL", 5)

# Sell some shares
account.sell_shares("AAPL", 2)

# Calculate portfolio value
portfolio_value = account.calculate_portfolio_value()

# Check profit or loss
profit_loss = account.calculate_profit_loss()

# Get current holdings
holdings = account.get_holdings()

# List transactions
transactions = account.get_transactions()
```

### Constraints:

- Prevent withdrawals that would result in negative balance.
- Prevent buying of shares without sufficient balance.
- Prevent selling of shares not owned by the user.

This design ensures robust account management functionality for a simulated trading platform, adhering to the stated requirements.
