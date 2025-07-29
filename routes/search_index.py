# 📁 File: smartswasthya/routes/search_index.py

import os
from fastapi import APIRouter
from flask import Blueprint, request, jsonify
from logic.search_logic import mock_search_results
from tools.smart_marker_injector import auto_route
from tools.obvious_router import auto_route

search_bp = Blueprint("search", __name__, url_prefix="/search")

router = APIRouter()

@search_bp.route("/", methods=["GET"])
@auto_route
def search_handler():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Missing ?q parameter"}), 400
    results = mock_search_results(query)
    return jsonify({"query": query, "results": results})
