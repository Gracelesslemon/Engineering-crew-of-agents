import datetime

def get_share_price(symbol: str) -> float:
    """Returns the current price of the given stock."""
    if symbol == "AAPL":
        return 170.0
    elif symbol == "TSLA":
        return 800.0
    elif symbol == "GOOGL":
        return 2600.0
    else:
        return 100.0  # Default price

class Account:
    """Represents a user's trading account."""

    def __init__(self, account_id: str):
        """Initializes a new account."""
        self.account_id = account_id
        self.balance = 0.0
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = 0.0
        self.creation_timestamp = datetime.datetime.now()

    def deposit(self, amount: float) -> bool:
        """Adds funds to the account balance."""
        if amount > 0:
            self.balance += amount
            self._record_transaction("deposit", amount=amount)
            if self.initial_deposit == 0.0:
                self.initial_deposit = amount
            return True
        return False

    def withdraw(self, amount: float) -> bool:
        """Subtracts funds from the account balance."""
        if 0 < amount <= self.balance:
            self.balance -= amount
            self._record_transaction("withdraw", amount=amount)
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        """Purchases shares of a given stock."""
        price = get_share_price(symbol)
        cost = price * quantity
        if cost <= self.balance and quantity > 0:
            self.balance -= cost
            if symbol in self.holdings:
                self.holdings[symbol] += quantity
            else:
                self.holdings[symbol] = quantity
            self._record_transaction("buy", symbol=symbol, quantity=quantity, price=price)
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        """Sells shares of a given stock."""
        if symbol in self.holdings and self.holdings[symbol] >= quantity and quantity > 0:
            price = get_share_price(symbol)
            revenue = price * quantity
            self.balance += revenue
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self._record_transaction("sell", symbol=symbol, quantity=quantity, price=price)
            return True
        return False

    def get_balance(self) -> float:
        """Returns the current account balance."""
        return self.balance

    def get_holdings(self) -> dict:
        """Returns a dictionary representing the user's current stock holdings."""
        return self.holdings

    def get_portfolio_value(self) -> float:
        """Calculates and returns the total value of the user's portfolio."""
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_loss(self) -> float:
        """Calculates and returns the profit or loss since the account's creation."""
        initial_investment = self.initial_deposit
        if not self.initial_deposit and not self.transactions: # No initial deposit and no transactions, no profit/loss to calculate
            return 0.0
        portfolio_value = self.get_portfolio_value()
        profit_loss = portfolio_value - initial_investment
        return profit_loss

    def get_transactions(self) -> list:
        """Returns a list of all transactions performed on the account."""
        return self.transactions

    def _record_transaction(self, type: str, symbol: str = None, quantity: int = None, price: float = None, amount: float = None):
        """Appends a transaction record to the transactions list."""
        transaction = {"type": type, "timestamp": datetime.datetime.now().isoformat() }
        if symbol:
            transaction["symbol"] = symbol
        if quantity is not None:
            transaction["quantity"] = quantity
        if price is not None:
            transaction["price"] = price
        if amount is not None:
            transaction["amount"] = amount
        self.transactions.append(transaction)
