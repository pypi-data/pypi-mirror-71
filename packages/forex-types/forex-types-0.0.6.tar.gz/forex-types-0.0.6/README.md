# python_forex_types
Class models for Eight major Forex Currency Pairs.



### Summary of Classes provided
class | init example | description
 --- | --- | ---
 Calc | -- | Has class methods for doing calculations with other types.
 Cash | Cash("102.231", Currency.JPY) | Cash represented by decimal number and currency.
 Currency | Currency("EUR") | EUR, GBP, AUD, NZD, USD, CAD, CHF or JPY
 FracPips | FracPips(112345) | Integer subclass for fractional pips.
 LotSize | LotSize(20000) | Integer subclass for number of units in trade.
 Pair | Pair("AUD_USD") | one of 28 forex pairs from the 8 currencies
 Price | Price("1.2342") | Decimal based representation of forex price.
 
### Quick Example
```python
from forex_types import Pair, Currency, Price, LotSize, Calc, Direction

# Details of trade:
pair = Pair.EUR_USD
lot_size = LotSize(20000)
direction = Direction.LONG
entry_price = Price("1.2223")
exit_price = Price("1.2244")

# Figuring out the profit (or loss)
profit = Calc.get_trade_cash(lot_size, pair.quote, direction, entry_price, exit_price)

print(f"Trade Result: {profit.nearest_cent()}")
```

### Quick note about Price class
Although the `Price` class represents price, it does not know its quote
currency. When constructed it determines if the price is in a Japanese Yen
kind of range, and if so a subclass called `NinjaPrice` is returned, otherwise
if it is in a reasonable range for other currencies a `Price` object is returned.
If the price is out of what is considered a reasonable range, an exception is raised.
Note that an important difference between Japanese Yen based currencies is that
there are 100 pips to a Yen, but for our other currencies there are 10,000
pips per unit.


### Disclaimers:
1. Only the eight major currencies are supported with the resulting 28 currency
pairs. This might be expanded to include other currencies that are reasonably stable and
whose central banks establish a record of responsibly managing them (the CHF is
supported with a reluctant eye to that business with the Euro peg in 2015--but
with the trust they have learned their lesson).
1. There is no plan to ever support any crypto currency. Nor is there any chain
saw juggling support for similar reasons.
1. no API to any data or broker in this package. However, there is a
separate [oanda-candles API](https://pypi.org/project/oanda-candles/)
that is built on this package.
1. The `Calc` class needs some more functionality. In particular, a function
that converts one currency into another given the relevant forex price.
1. There are parts that are not covered by unit tests and are a bit rough and
likely to be changed in future updates.



