import requests
from typing import Dict, Any
import os

from src.domain.interfaces.gateways.payment_gateway import PaymentGateway
from src.domain.value_objects.payment_result import PaymentResult
from src.infrastructure.mappers.blumonpay_error_mapper import BlumonpayErrorMapper
from src.presentation.dtos.transaction_dto import CreateTransactionDTO


class BlumonpayPaymentGateway(PaymentGateway):
    def __init__(self):
        self.api_url = os.getenv("BLUMONPAY_API_URL")
        self.payment_endpoint = os.getenv("BLUMONPAY_PAYMENT_ENDPOINT")
        self.token_url = os.getenv("BLUMONPAY_TOKEN_URL")
        self.credentials = os.getenv("BLUMONPAY_BASIC_TOKEN")
        self.username = os.getenv("BLUMONPAY_USER")
        self.password = os.getenv("BLUMONPAY_PASSWORD")
        self.prepared_data = {}
        self.token = self.authenticate(credentials=self.credentials, username=self.username, password=self.password)

    def authenticate(self, credentials: str, username: str, password: str) -> str:
        """Autentica con la API de Blumonpay y retorna un token de acceso."""
        headers = {
            'Authorization': f'Basic {credentials}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'HttpOnly'
        }
        payload = f'grant_type=password&username={username}&password={password}'
        response = requests.post(self.token_url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()['access_token']

    def prepare_data(self, payment_data: CreateTransactionDTO) -> Dict[str, Any]:
        """Prepara los datos para ser enviados a Blumonpay."""
        # Mapear los datos del DTO al formato específico requerido por Blumonpay
        self.prepared_data = {
            "amount": float(payment_data.amount),
            "currency": payment_data.currency,
            "customerInformation": {
                "firstName": payment_data.customer_information.first_name,
                "lastName": payment_data.customer_information.last_name,
                "middleName": payment_data.customer_information.middle_name,
                "email": payment_data.customer_information.email,
                "phone1": payment_data.customer_information.phone,
                "city": payment_data.customer_information.city,
                "address1": payment_data.customer_information.address,
                "postalCode": payment_data.customer_information.postal_code,
                "state": payment_data.customer_information.state,
                "country": payment_data.customer_information.country,
                "ip": payment_data.customer_information.ip
            },
            "noPresentCardData": {
                "cardNumber": payment_data.card_information.card_number,
                "cvv": payment_data.card_information.cvv,
                "cardholderName": payment_data.card_information.card_holder_name,
                "expirationYear": payment_data.card_information.expiration_year,
                "expirationMonth": payment_data.card_information.expiration_month
            }
        }

    def process_payment(self) -> Dict[str, Any]:
        """Envía los datos del pago a Blumonpay y retorna la respuesta."""
        headers = {'Authorization': f'Bearer {self.token}'}
        payment_url = f"{self.api_url}{self.payment_endpoint}"
        response = requests.post(payment_url, json=self.prepared_data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if not response_data.get('status'):
                blumonpay_error_mapper = BlumonpayErrorMapper()
                error_details = response_data.get('error', {})
                error_code = error_details.get('code')
                error_description = error_details.get('description', 'Unknown error')
                raise blumonpay_error_mapper.map_error_to_exception(error_code, error_description)

            authorization = response_data.get('dataResponse', {}).get('authorization', 'No authorization found')
            status = response_data.get('dataResponse', {}).get('description', 'No description found')
            return PaymentResult(
                status=status,
                id=authorization
            )

        raise Exception("Internal Server Error. Please try again or contact support.")

