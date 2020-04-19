from decimal import Decimal, ROUND_DOWN

from settings import settings


def quantize(
        var: Decimal,
        precision=settings.decimal_precision,
        rounding=ROUND_DOWN,
) -> Decimal:
    return var.quantize(Decimal(f'.{"0" * (precision - 1)}1'), rounding=rounding)
