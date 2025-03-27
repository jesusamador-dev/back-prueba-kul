from src.domain.interfaces.gateways.payment_gateway import PaymentGateway
from src.domain.entities.transaction import Transaction
from src.domain.interfaces.repositories.transactions_repository import TransactionsRepository
from src.presentation.dtos.transaction_dto import CreateTransactionDTO
from src.domain.errors.payment_processing_error import PaymentProcessingError
from fastapi import HTTPException


class CreateTransactionUseCase:
    def __init__(self, payment_gateway: PaymentGateway,
                 transactions_repository: TransactionsRepository):
        """
        Inicializa el caso de uso con una instancia de un gateway de pagos.

        :param payment_gateway: Una instancia de PaymentGateway que se encargará de procesar el pago.
        """
        self.payment_gateway = payment_gateway
        self.transactions_repository = transactions_repository

    async def execute(self, transaction_data: CreateTransactionDTO):
        """
        Ejecuta el caso de uso para crear una transacción.

        :param transaction_data: Un diccionario con los datos necesarios para la transacción.
        :return: Un diccionario con el resultado del proceso de la transacción.
        """
        try:
            # Paso 1: Preparar modelo de datos
            transaction = Transaction(
                amount=float(transaction_data.amount),
                currency=transaction_data.currency,
                customer_name=transaction_data.customer_information.first_name,
                customer_email=transaction_data.customer_information.email,
                status="",
                gateway_transaction_id=""
            )

            # Paso 2: Cambiar el formato del currency
            transaction_data.currency = transaction.convert_currency_iso_to_code()

            # Paso 3: Parsear y preparar los datos para el pago
            self.payment_gateway.prepare_data(transaction_data)

            # Paso 4: Procesar el pago con los datos preparados
            payment_result = self.payment_gateway.process_payment()
            transaction.status = payment_result.status
            transaction.gateway_transaction_id = payment_result.id

            # Paso 5: Guardar en nuestra base de datos
            self.transactions_repository.save(transaction=transaction)

            return payment_result
        except PaymentProcessingError as e:
            raise HTTPException(status_code=400, detail=e.message)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error. Please try again or contact support.")
