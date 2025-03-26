from src.domain.errors.payment_processing_error import PaymentProcessingError


class InsufficientFundsError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Fondos insuficientes", code=51)

class CardExpiredError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Tarjeta vencida", code=54)

class InvalidPinError(PaymentProcessingError):
    def __init__(self):
        super().__init__("PIN inválido", code=55)

class PaymentNotAllowedError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Pago no permitido por el emisor", code=57)

class TransactionLimitExceededError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Límite de transacción excedido", code=61)

class TransactionNotAllowedError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Transacción no permitida", code=62)

class PinAttemptsExceededError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Intentos de PIN excedidos", code=106)

class InvalidTransactionDataError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Datos de transacción inválidos", code=110)

class AccountInvalidError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Cuenta no válida", code=111)

class OperationNotAllowedError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Operativa no válida", code=115)

class SecurityCodeInvalidError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Código de seguridad no válido", code=122)

class DateInvalidError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Fecha no válida", code=125)

class CardInactiveError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Tarjeta no activa", code=187)

class CardInvalidError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Tarjeta inválida", code=200)

class TransactionDeniedError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Transacción denegada", code=904)

class IssuerUnavailableError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Emisor no disponible", code=912)

class OriginalTransactionNotFoundError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Transacción original no encontrada", code=914)

class AccountCanceledError(PaymentProcessingError):
    def __init__(self):
        super().__init__("Cuenta cancelada", code=188)


class TransactionDuplicateError(PaymentProcessingError):
    def __init__(self, message="Transaction duplicate"):
        super().__init__(message, code=94)
