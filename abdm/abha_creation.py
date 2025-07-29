# 📁 File: smartswasthya/abdm/abha_creation.py

import requests
from .sandbox_config import ABHA_APIS, SANDBOX_HEADERS, SANDBOX_AUTH_TOKEN

def generate_mobile_otp(mobile_number: str):
    url = ABHA_APIS["generate_mobile_otp"]
    payload = {
        "mobile": mobile_number
    }
    headers = SANDBOX_HEADERS.copy()
    headers["Authorization"] = SANDBOX_AUTH_TOKEN

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def verify_mobile_otp(txnId: str, otp: str):
    url = ABHA_APIS["verify_mobile_otp"]
    payload = {
        "otp": otp,
        "txnId": txnId
    }
    headers = SANDBOX_HEADERS.copy()
    headers["Authorization"] = SANDBOX_AUTH_TOKEN

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def create_abha_address(pre_verified_txnId: str, abha_username: str):
    url = ABHA_APIS["create_abha_address"]
    payload = {
        "txnId": pre_verified_txnId,
        "phrAddress": abha_username
    }
    headers = SANDBOX_HEADERS.copy()
    headers["Authorization"] = SANDBOX_AUTH_TOKEN

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
