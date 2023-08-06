import logging
from typing import Union
from urllib.parse import urljoin

from .types import DateType, PaddleJsonType
from .validators import validate_date

log = logging.getLogger(__name__)


def list_subscription_payments(
    self,
    subscription_id: int = None,
    plan: int = None,
    is_paid: Union[bool, int] = None,
    _from: DateType = None,
    to: DateType = None,
    is_one_off_charge: bool = None,
) -> dict:
    """
    https://developer.paddle.com/api-reference/subscription-api/payments/listpayments
    """
    url = urljoin(self.vendors_v2, 'subscription/payments')

    json = {
        'subscription_id': subscription_id,
        'plan': plan,
        'is_one_off_charge': is_one_off_charge,
    }  # type: PaddleJsonType
    if is_paid and isinstance(is_paid, bool):
        json['is_paid'] = 1 if is_paid else 0
    if _from:
        json['from'] = validate_date(_from, '_from')
    if to:
        json['to'] = validate_date(to, 'to')

    return self.post(url=url, json=json)


def reschedule_subscription_payment(
    self,
    payment_id: int,
    date: DateType,
) -> dict:
    """
    https://developer.paddle.com/api-reference/subscription-api/payments/updatepayment
    """
    url = urljoin(self.vendors_v2, 'subscription/payments_reschedule')

    json = {
        'payment_id': payment_id,
        'date': validate_date(date, 'date'),
    }  # type: PaddleJsonType
    return self.post(url=url, json=json)
