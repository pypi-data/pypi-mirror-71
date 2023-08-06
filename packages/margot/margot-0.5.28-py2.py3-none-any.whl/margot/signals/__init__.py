from margot.signals.algos import BaseAlgo


class Position(object):
    """Represents a Position with a symbol and a weight.

    Arguments:
        symbol (str): The identifier of the symbol. e.g. 'SPY'.
        weight (float): A value between -1.0 and +1.0 representing
                        the weight of this symbol in the position list.
    """

    def __init__(self, symbol: str, weight: float):  # noqa: D107
        self.symbol = symbol
        self.weight = weight

    def __repr__(self):
        """Represent."""
        return str((self.symbol, self.weight))
