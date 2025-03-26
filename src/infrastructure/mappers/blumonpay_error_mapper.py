from src.domain.errors.payments_errors import *


class BlumonpayErrorMapper:
    def __init__(self):
        self.error_mapping = {
            51: InsufficientFundsError(),
            54: CardExpiredError(),
            55: InvalidPinError(),
            57: PaymentNotAllowedError(),
            61: TransactionLimitExceededError(),
            62: TransactionNotAllowedError(),
            65: TransactionLimitExceededError(),
            75: InvalidPinError(),
            94: TransactionDuplicateError(),
            'N5': TransactionNotAllowedError(),
            'O4': TransactionLimitExceededError(),
            101: CardExpiredError(),
            106: PinAttemptsExceededError(),
            110: InvalidTransactionDataError(),
            111: AccountInvalidError(),
            115: OperationNotAllowedError(),
            117: InvalidPinError(),
            122: SecurityCodeInvalidError(),
            125: DateInvalidError(),
            187: CardInactiveError(),
            200: CardInvalidError(),
            904: TransactionDeniedError(),
            912: IssuerUnavailableError(),
            914: OriginalTransactionNotFoundError(),
            188: AccountCanceledError()
        }

    def map_error_to_exception(self, error_code: str, error_desc: str):
        """Mapea los códigos de error de Blumonpay a excepciones personalizadas."""
        exception_class = self.error_mapping.get(error_code, PaymentProcessingError)
        return exception_class(f"Error {error_code}: {error_desc}")
