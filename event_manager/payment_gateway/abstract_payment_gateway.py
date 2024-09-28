from abc import ABC, abstractmethod
from typing import Any, Dict


class PaymentGateway(ABC):
    @abstractmethod
    def create_payment_intent(
        self, amount: int, currency: str | None = "INR", metadata: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def handle_webhook_event(self, event: Dict[str, Any], db: Any) -> None:
        pass
