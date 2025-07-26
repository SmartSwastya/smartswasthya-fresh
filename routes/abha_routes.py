# 📁 File: smartswasthya/routes/abha_routes.py

import os
from fastapi import APIRouter
from flask import Blueprint, request, jsonify
from abdm.abha_creation import generate_mobile_otp, verify_mobile_otp, create_abha_address
from abdm.consent_manager import initiate_consent_request, check_consent_status, handle_consent_notification
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route

abha_bp = Blueprint('abha', __name__, url_prefix='/api/abdm')

router = APIRouter()

@abha_bp.route('/generate-otp', methods=['POST'])
@auto_route
def generate_otp_route():
    data = request.json
    mobile = data.get("mobile")
    if not mobile:
        return jsonify({"error": "Missing mobile number"}), 400
    result = generate_mobile_otp(mobile)
    return jsonify(result)

@abha_bp.route('/verify-otp', methods=['POST'])
@auto_route
def verify_otp_route():
    data = request.json
    txnId = data.get("txnId")
    otp = data.get("otp")
    if not txnId or not otp:
        return jsonify({"error": "Missing txnId or otp"}), 400
    result = verify_mobile_otp(txnId, otp)
    return jsonify(result)

@abha_bp.route('/create-abha', methods=['POST'])
@auto_route
def create_abha_route():
    data = request.json
    txnId = data.get("txnId")
    phrAddress = data.get("phrAddress")
    if not txnId or not phrAddress:
        return jsonify({"error": "Missing txnId or phrAddress"}), 400
    result = create_abha_address(txnId, phrAddress)
    return jsonify(result)

@abha_bp.route('/consent/initiate', methods=['POST'])
@auto_route
def initiate_consent():
    consent_body = request.json
    result = initiate_consent_request(consent_body)
    return jsonify(result)

@abha_bp.route('/consent/status', methods=['POST'])
@auto_route
def consent_status():
    data = request.json
    consent_id = data.get("consentRequestId")
    if not consent_id:
        return jsonify({"error": "Missing consentRequestId"}), 400
    result = check_consent_status(consent_id)
    return jsonify(result)

@abha_bp.route('/on-notify', methods=['POST'])
@auto_route
def consent_notify():
    notification = request.json
    result = handle_consent_notification(notification)
    return jsonify(result)
