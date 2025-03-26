from abc import ABC, abstractmethod
from typing import Dict, Optional, Any


class PaymentGateway(ABC):


    @abstractmethod
    def process_payment(self) -> Dict[str, any]:
        """
        Procesa un pago a través del gateway de pago.

        Args:
        amount (float): Cantidad del pago.
        currency (str): Moneda del pago.
        customer_details (Dict[str, str]): Detalles del cliente, incluyendo email y nombre.
        card_details (Dict[str, str]): Detalles de la tarjeta, como el bin y last4.

        Returns:
        Dict[str, any]: Resultado del proceso de pago que incluye status y transaction_id.
        """
        pass

    def prepare_data(self, payment_dto: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepara los datos para el proceso de pago.

        Args:
        payment_dto (Dict[str, Any]): DTO que contiene todos los detalles necesarios para el pago.

        Returns:
        Dict[str, Any]: Datos preparados para ser procesados.
        """
        pass
