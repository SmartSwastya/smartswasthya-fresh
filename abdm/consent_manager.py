# 📁 File: smartswasthya/abdm/consent_manager.py

import requests
from .sandbox_config import CONSENT_APIS, SANDBOX_HEADERS, SANDBOX_AUTH_TOKEN

def initiate_consent_request(consent_request_body: dict):
    """
    Accepts a properly formatted consentRequest body (FHIR-compliant),
    and initiates consent via ABDM gateway.
    """
    url = CONSENT_APIS["request"]
    headers = SANDBOX_HEADERS.copy()
    headers["Authorization"] = SANDBOX_AUTH_TOKEN

    response = requests.post(url, json=consent_request_body, headers=headers)
    return response.json()

def check_consent_status(consent_id: str):
    """
    Poll consent request status using consent-request ID
    """
    url = CONSENT_APIS["status"]
    headers = SANDBOX_HEADERS.copy()
    headers["Authorization"] = SANDBOX_AUTH_TOKEN

    payload = { "consentRequestId": consent_id }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def handle_consent_notification(notification_body: dict):
    """
    This function will process the `on-notify` payload from ABDM gateway.
    To be used in /api/abdm/on-notify POST endpoint.
    """
    # Extract consent artifacts or status from notification_body
    return {
        "status": "received",
        "data": notification_body
    }
