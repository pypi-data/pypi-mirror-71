from see137.utils.trades import TradeType

class TradePercentage(object):
    """A trade object for use within trading environments."""

    def __init__(self, symbol: str, trade_type: 'TradeType', percentage=0.4):
        """
        Arguments:
            symbol: The exchange symbol of the instrument in the trade (AAPL, ETH/USD, NQ1!, etc).
            trade_type: The type of trade executed (0 = HOLD, 1=LIMIT_BUY, 2=MARKET_BUY, 3=LIMIT_SELL, 4=MARKET_SELL).
            amount: The amount of the instrument in the trade (shares, satoshis, contracts, etc).
            price: The price paid per instrument in terms of the base instrument (e.g. 10000 represents $10,000.00 if the `base_instrument` is "USD").
        """
        self._symbol = symbol
        self._trade_type = trade_type
        self._percentage = percentage
        self._amount = 0.0
        self._price = 0.0

    def copy(self) -> 'TradePercentage':
        """Return a copy of the current trade object."""
        return TradePercentage(symbol=self._symbol, trade_type=self._trade_type, percentage=self._percentage)

    
    @property
    def symbol(self) -> str:
        """The exchange symbol of the instrument in the trade (AAPL, ETH/USD, NQ1!, etc)."""
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str):
        self._symbol = symbol

    @property
    def trade_type(self) -> 'TradeType':
        """The type of trade ("buy", "sell", "hold", etc)."""
        return self._trade_type

    @trade_type.setter
    def trade_type(self, trade_type: 'TradeType'):
        self._trade_type = trade_type

    @property
    def amount(self) -> float:
        """The amount of the instrument in the trade (shares, satoshis, contracts, etc)."""
        return self._amount

    @amount.setter
    def amount(self, amount: float):
        self._amount = amount


    @property
    def is_hold(self) -> bool:
        """
        Returns:
            Whether the trade type is non-existent (i.e. hold).
        """
        return self._trade_type.is_hold

    @property
    def is_buy(self) -> bool:
        """
        Returns:
            Whether the trade type is a buy offer.
        """
        return self._trade_type.is_buy

    @property
    def is_sell(self) -> bool:
        """
        Returns:
            Whether the trade type is a sell offer.
        """
        return self._trade_type.is_sell