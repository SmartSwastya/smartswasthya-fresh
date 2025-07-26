# 📁 File: smartswasthya/abdm/phr_gateway.py

import requests
from .sandbox_config import SANDBOX_HEADERS, SANDBOX_AUTH_TOKEN

def link_phr_address(abha_number: str, phr_address: str, txn_id: str):
    """
    Link ABHA Number with given PHR address (username) during ABHA creation.
    """
    url = "https://dev.abdm.gov.in/gateway/v0.5/phr-address"
    headers = SANDBOX_HEADERS.copy()
    headers["Authorization"] = SANDBOX_AUTH_TOKEN

    payload = {
        "abhaNumber": abha_number,
        "phrAddress": phr_address,
        "txnId": txn_id
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def fetch_linked_phr(abha_number: str):
    """
    Fetch list of PHR addresses already linked to this ABHA number.
    """
    url = f"https://dev.abdm.gov.in/gateway/v0.5/account/phr-address/{abha_number}"
    headers = SANDBOX_HEADERS.copy()
    headers["Authorization"] = SANDBOX_AUTH_TOKEN

    response = requests.get(url, headers=headers)
    return response.json()
