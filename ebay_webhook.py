#!/usr/bin/env python3
"""
eBay Marketplace Account Deletion Notification Endpoint
Deployed on Render.com: https://ebay-webhook-kbuq.onrender.com
"""

import hashlib, os, json
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFICATION_TOKEN = "ebay-dropship-d4zvW4jeuetvruyxC5k80dUxuQ7yc6hX"


@app.route("/", methods=["GET"])
def health():
    return "eBay webhook OK", 200


@app.route("/ebay/notifications", methods=["GET", "POST"])
def notifications():
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code", "")
        # Compute endpoint URL dynamically; force https (Render terminates TLS at proxy)
        endpoint_url = request.base_url.replace("http://", "https://")
        digest = hashlib.sha256(
            f"{challenge_code}{VERIFICATION_TOKEN}{endpoint_url}".encode()
        ).hexdigest()
        return jsonify({"challengeResponse": digest})

    try:
        payload = request.get_json(silent=True) or {}
        print(f"[eBay notification] {json.dumps(payload)[:200]}")
    except Exception:
        pass
    return ("", 200)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
