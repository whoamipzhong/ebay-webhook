#!/usr/bin/env python3
"""
eBay Marketplace Account Deletion Notification Endpoint
Deploy to Render.com (free tier) to get a public HTTPS URL.

Setup:
  1. Deploy this file to Render.com as a Web Service
  2. Set ENDPOINT_URL below to your actual Render URL
  3. Fill the Alerts & Notifications page on developer.ebay.com
"""

import hashlib, os, json
from flask import Flask, request, jsonify

app = Flask(__name__)

# ── MUST match what you entered on developer.ebay.com ─────────────────────────
VERIFICATION_TOKEN = "ebay-dropship-d4zvW4jeuetvruyxC5k80dUxuQ7yc6hX"
ENDPOINT_URL       = os.environ.get(
    "ENDPOINT_URL",
    "https://ebay-webhook-kbuq.onrender.com/ebay/notifications"   # ← update after deploy
)


@app.route("/", methods=["GET"])
def health():
    return "eBay webhook OK", 200


@app.route("/ebay/notifications", methods=["GET", "POST"])
def notifications():
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code", "")
        digest = hashlib.sha256(
            f"{challenge_code}{VERIFICATION_TOKEN}{ENDPOINT_URL}".encode()
        ).hexdigest()
        return jsonify({"challengeResponse": digest})

    # POST — actual account deletion notification; just acknowledge
    try:
        payload = request.get_json(silent=True) or {}
        print(f"[eBay notification] {json.dumps(payload)[:200]}")
    except Exception:
        pass
    return ("", 200)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
