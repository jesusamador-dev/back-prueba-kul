from src.domain.interfaces.gateways.payment_gateway import PaymentGateway
from src.domain.entities.transaction import Transaction
from src.domain.interfaces.repositories.transactions_repository import TransactionsRepository
from src.presentation.dtos.transaction_dto import CreateTransactionDTO


class CreateTransactionUseCase:
    def __init__(self, payment_gateway: PaymentGateway,
                 transactions_repository: TransactionsRepository):
        """
        Inicializa el caso de uso con una instancia de un gateway de pagos.

        :param payment_gateway: Una instancia de PaymentGateway que se encargará de procesar el pago.
        """
        self.payment_gateway = payment_gateway
        self.transactions_repository = transactions_repository

    def execute(self, transaction_data: CreateTransactionDTO):
        """
        Ejecuta el caso de uso para crear una transacción.

        :param transaction_data: Un diccionario con los datos necesarios para la transacción.
        :return: Un diccionario con el resultado del proceso de la transacción.
        """
        # Paso 1: Parsear y preparar los datos para el pago
        self.payment_gateway.prepare_data(transaction_data)

        # Paso 2: Procesar el pago con los datos preparados
        payment_result = self.payment_gateway.process_payment()

        # Paso 3: Preparar modelo de datos
        transaction = Transaction(
            amount=float(transaction_data.amount),
            currency=transaction_data.currency,
            customer_name=transaction_data.customer_information.first_name,
            customer_email=transaction_data.customer_information.email,
            status="",
            gateway_transaction_id=""
        )

        # Paso 4: Guardar en nuestra base de datos
        self.transactions_repository.save(transaction=transaction)

        return payment_result
