# EOQ.py
import math
from numbers import Number

class ErrorEOQ(Exception):
    """
    EOQ specific exception that can be raised whenever an invalid argument is attempted for an EOQ object.
    """

    def __init__(self, msg: str, *args):
        """
        ErrorEOQ specific constructor
        :param msg: Message for customizing the information raised.
        :type msg: str
        :param args: variable argument list passed to Exception's constructor
        :type args: list
        """
        super().__init__(args)
        self.msg = msg


    def __repr__(self):
        """
        Console representation of the exception
        :return: Pretty representation
        :rtype: str
        """
        return f'\nException: {type(self)} - {self.msg}\n'


    def __str__(self):
        """
        Print representation of the exception
        :return: Pretty representation
        :rtype: str
        """
        return self.__repr__()


class EOQItem:
    """
    The EOQItem class represents an EOQ item for managing replenishment. The class encapsulates the EOQ model parameters
    and provides methods obtaining:
    - Q - the economic order quantity
    - TRC - the total relevant cost of the inventory policy
    - ATC - the annual total cost of the inventory policy (TRC + acquisition cost)
    """

    def __init__(self, d: Number, a: Number, v: Number, r: Number, oh: Number = 0, oo: Number = 0) -> None:
        """
        EOQ constructor. Raises ErrorEOQ if any of the following required arguments are invalid:
        :param d: demand (units/unit time)
        :param a: aggregate cost per order (independent of quantity ordered)
        :param v: unit acquisition cost
        :param r: unit holding cost percentage rate (per unit time)
        :param oh: Units on hand (default 0)
        :param oo: Units on order (default 0)
        :return: None
        """

        # All arguments are valid so we can construct the EOQ object using the setters, where existing, so
        # that construction validation is the same as assignment validation. The setters will also set the
        # recalculation state to True (recalculation needed).

        # EOQ model parameters - less volatile state
        self.d = d
        self.a = a
        self.v = v
        self.r = r

        # EOQItem volatile state
        if oh >= 0:
            self._oh = oh
        else:
            raise ErrorEOQ(f'Terminal error! Units on hand (oh) must be numeric and positive.')

        if oo >= 0:
            self._oo = oo
        else:
            raise ErrorEOQ(f'Terminal error! Units on hand (oh) must be numeric and positive.')

    def __repr__(self) -> str:
        """
        Console representation of EOQ object.
        :return: Prettified EOQ representation
        """

        return (f'{type(self)} at {id(self)}: d={self.d}, a={self.a}, v={self.v}, r={self.r}, '
                f'oh={self.oh}, oo={self.oo}, recalc_needed={self.recalc_needed}')

    def __str__(self) -> str:
        """
        Print representation of EOQ object.
        :return: Prettified EOQ representation for print()
        """

        return f'{type(self)} at {id(self)}: \n\td={self.d}, \n\ta={self.a}, \n\tv={self.v}, \n\tr={self.r}, ' \
               f'\n\toh={self.oh}, \n\too={self.oo}, \n\trecalc_needed={self.recalc_needed}'

    @property
    def a(self) -> Number:
        """
        Aggregate order cost getter.

        :return: Aggregate order cost (a)
        """

        return self._a

    @a.setter
    def a(self, a: Number) -> None:
        """
        Aggregate order cost setter. Ensures a is numeric and positive or raises an ErrorEOQ exception.
        :param Aggregate order cost (a):
        :return: None
        """
        if not isinstance(a, Number) or a <= 0:
            raise ErrorEOQ(f'Terminal error! Aggregate order cost (a) must be numeric and positive.')
        else:
            self._recalc_needed = True
            self._a = a

    @property
    def d(self) -> Number:
        """
        Demand getter.
        :return: Demand (d)
        """

        return self._d

    @d.setter
    def d(self, d: Number) -> None:
        """
        Demand setter. Ensures d is numeric and positive or raises an ErrorEOQ exception.
        :param d:
        :return: None
        """
        if not isinstance(d, Number) or d <= 0:
            raise ErrorEOQ(f'Terminal error! Demand (d) must be numeric and positive.')
        else:
            self._recalc_needed = True
            self._d = d

    @property
    def oh(self) -> Number:
        """
        On hand units (oh) getter.

        :return: on hand units (oh)
        """

        return self._oh

    @property
    def oo(self) -> Number:
        """
        On order (with supplier) units (oo) getter.

        :return: on order units (oo)
        """

        return self._oo

    @property
    def r(self) -> Number:
        """
        Unit holding cost percentage rate getter.
        :return: Unit holding cost percentage rate (r)
        """

        return self._r

    @r.setter
    def r(self, r: Number) -> None:
        """
        Unit holding cost percentage rate setter. Ensures r is numeric and positive or raises an ErrorEOQ exception.
        :param r:
        :return: None
        """
        if not isinstance(r, Number) or r <= 0:
            raise ErrorEOQ(f'Terminal error! Unit holding cost percentage rate (r) must be numeric and positive.')
        else:
            self._recalc_needed = True
            self._r = r

    @property
    def recalc_needed(self) -> bool:
        """
        Recalculation state getter.
        :return: Recalculation state
        """

        return self._recalc_needed

    @property
    def v(self) -> Number:
        """
        Unit acquisition cost getter.
        :return: Unit acquisition cost (a)
        """

        return self._v

    @v.setter
    def v(self, v: Number) -> None:
        """
        Unit acquisition cost setter. Ensures v is numeric and positive or raises an ErrorEOQ exception.
        :param v:
        :return: None
        """
        if not isinstance(v, Number) or v <= 0:
            raise ErrorEOQ(f'Terminal error! Unit acquisition cost (v) must be numeric and positive.')
        else:
            self._recalc_needed = True
            self._v = v

    def _calculate(self) -> None:
        """
        Private recalculation method, called before returning any metric when recalculation is required
        (i.e., whenever any EOQ argument has changed)

        :return: None
        """

        # recalculate all EOQ metrics. No rounding applied so that calling application can control rounding
        self._q = math.sqrt(2 * self.d * self.a / (self.v * self.r))
        self._trc = math.sqrt(2 * self.d * self.a * self.v * self.r)
        self._atc = self._trc + self.d * self.v

        # Calculations have been completed, so change recalculation state to recalc NOT needed
        self._recalc_needed = False

    def atc(self) -> Number:
        """
        Annual total cost (ATC) resulting from purchasing the cost minimizing order quantity.
        :return Annual total cost:
        """

        if self.recalc_needed:
            self._calculate()

        return self._atc

    def decrease_oh(self, qty=1) -> Number:
        """
        Decreases the oh inventory balance by the specified quantity. Does not allow for negative oh.
        :param qty: quantity to be removed from oh balance.
        :return: new oh.
        """

        if not isinstance(qty, Number) or qty < 0:
            raise ErrorEOQ(f'Terminal error! Unit quantity (qty) must be numeric and non-negative.')

        # qty is ok so decrement oh but prevent negative on hand
        self._oh = max(0, self._oh - qty)
        return self.oh

    def decrease_oo(self, qty=1) -> Number:
        """
        Decreases the oo inventory balance by the specified quantity. Does not allow for negative oo.
        :param qty: quantity to be removed from oo balance.
        :return: New oo.
        """

        if not isinstance(qty, Number) or qty < 0:
            raise ErrorEOQ(f'Terminal error! Unit quantity (qty) must be numeric and non-negative.')

        # qty is oo so decrement oo but prevent negative on hand
        self._oo = max(0, self._oo - qty)
        return self.oo

    def eoq(self) -> Number:
        """
        Economic order quantity (i.e., the cost minimizing order quantity)
        :return Economic order quantity:
        """

        if self.recalc_needed:
            self._calculate()

        return self._q

    def increase_oh(self, qty=1) -> Number:
        """
        Increases the oh inventory balance by the specified quantity.
        :param qty: quantity to be added to oh balance.
        :return: New oh.
        """

        if not isinstance(qty, Number) or qty < 0:
            raise ErrorEOQ(f'Terminal error! Unit quantity (qty) must be numeric and non-negative.')

        # qty is ok so increment oh
        self._oh += qty
        return self.oh

    def increase_oo(self, qty=1) -> bool:
        """
        Increases the oo inventory balance by the specified quantity.
        :param qty: quantity to be added to oo balance.
        :return: New oo.
        """

        if not isinstance(qty, Number) or qty < 0:
            raise ErrorEOQ(f'Terminal error! Unit quantity (qty) must be numeric and non-negative.')

        # qty is oo so increment oo
        self._oo += qty
        return self.oo

    def order_policy(self, precision: Number = 0.001) -> dict:
        """
        Returns the complete order policy (i.e., Q*) plus ATC and TRC as a dictionary
        :param precision: The precision for all metrics. Defaults to 0.001 (3 decimal places). If >= 1,
                          then 0 decimal places will be used.
        :return: Order policy (EOQ, TRC, ATC)
        """

        # calculate the number of decimal places (using ternary operator)
        dec = 0 if precision >= 1 else int(-math.log10(precision))

        rslt = {'Q': round(self.eoq(), dec),
                'TRC': round(self.trc(), dec),
                'ATC': round(self.atc(), dec),}

        return rslt

    def trc(self) -> Number:
        """
        Total relevant cost (TRC) resulting from purchasing the cost minimizing order quantity.
        :return Total relevant cost:
        """

        if self.recalc_needed:
            self._calculate()

        return self._trc

