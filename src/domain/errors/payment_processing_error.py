class PaymentProcessingError(Exception):
    """Excepción base para errores de procesamiento de pagos."""
    def __init__(self, message, code=None):
        super().__init__(message)
        self.message = message
        self.code = code
