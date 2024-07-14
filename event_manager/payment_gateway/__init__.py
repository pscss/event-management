import uuid

from event_manager.payment_gateway.abstract_payment_gateway import PaymentGateway
from event_manager.payment_gateway.stripe_payment import stripe_payment_gateway


def get_payment_gateway() -> PaymentGateway:
    return stripe_payment_gateway


def get_idempotency_key() -> str:
    return str(uuid.uuid4())
